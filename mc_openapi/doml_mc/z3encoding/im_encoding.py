from itertools import product
import re
from typing import Union

from z3 import (And, BoolSort, Const, Context, Datatype, DatatypeRef,
                DatatypeSortRef, ForAll, FuncDeclRef, Function, IntSort, Not,
                Or, Solver, EnumSort)

from mc_openapi.doml_mc.z3encoding.metamodel_encoding import mk_enum_sort_dict

from ..intermediate_model import IntermediateModel, MetaModel
from ..intermediate_model.metamodel import get_mangled_attribute_defaults
from .types import Refs, SortAndRefs
from ..utils import Iff

def mk_elem_sort_dict(
    im: IntermediateModel,
    z3ctx: Context,
    additional_elems: list[str] = []
) -> SortAndRefs:
    return mk_enum_sort_dict("Element", list(im) + additional_elems, z3ctx=z3ctx)


def def_elem_class_f_and_assert_classes(
    im: IntermediateModel,
    solver: Solver,
    elem_sort: DatatypeSortRef,
    elem: Refs,
    class_sort: DatatypeSortRef,
    class_: Refs,
) -> FuncDeclRef:
    """
    ### Effects
    This procedure is effectful on `solver`.
    """
    elem_class_f = Function("elem_class", elem_sort, class_sort)
    for ename, e in im.items():
        solver.assert_and_track(
            elem_class_f(elem[ename]) == class_[e.class_],
            f"elem_class {ename} {e.class_}",
        )
    return elem_class_f


def assert_im_attributes(
    attr_rel: FuncDeclRef,
    solver: Solver,
    im: IntermediateModel,
    mm: MetaModel,
    elems: Refs,
    attr_sort: DatatypeSortRef, # Relationship sort
    attrs: Refs, # Relationship data
    attr_data_sort: DatatypeSortRef, # Value sort
    strings: Refs,
    allow_placeholders: bool = False
) -> None:
    """
    ### Effects
    This procedure is effectful on `solver`.
    """

    def encode_attr_data(value: Union[str, int, bool]) -> DatatypeRef:
        if type(value) is str:
            return attr_data_sort.str(strings[value])  # type: ignore
        elif type(value) is int:
            return attr_data_sort.int(value)  # type: ignore
        else:  # type(v) is bool
            return attr_data_sort.bool(value)  # type: ignore
    
    def add_type_to_attrs(mm: MetaModel, attrs: dict):
        ret = {}
        for attr_k, attr_v in attrs.items():
            mm_pkgclass_k, mm_attr_k = re.search("^(.+?)::(.+?)$", attr_k).group(1, 2)
            mm_attrs = mm[mm_pkgclass_k].attributes
            mm_attr = mm_attrs[mm_attr_k]
            ret[attr_k] = attr_v, mm_attr.type, mm_attr.multiplicity
        return ret

    a = Const("a", attr_sort)
    d = Const("d", attr_data_sort)


    for esn, im_es in im.items():
        # print(f"== {im[esn].user_friendly_name} ==")
        # print("MM_attrs_default:\n", get_mangled_attribute_defaults(mm, im_es.class_))
        # print("IM_attrs:\n", add_type_to_attrs(mm, im_es.attributes))
        mm_attrs = get_mangled_attribute_defaults(mm, im_es.class_)
        im_attrs = add_type_to_attrs(mm, im_es.attributes)
        attr_data = mm_attrs | im_attrs
        # print("attr_data:\n", attr_data)

        # ==== DEBUG ====
        # Remove commons_DOMLElement::description since
        # it's polluting printed results
        try:
            attr_data.pop("commons_DOMLElement::description")
        except:
            pass
        # ===============

        # Create list of `And` assertions that will go in the `Or` below
        assn_list = []
        for attr_k, (attr_values, attr_type, attr_mult) in attr_data.items():
            if attr_values is not None:
                for attr_value in attr_values:
                    assn_list.append(
                        And(
                            a == attrs[attr_k],
                            d == encode_attr_data(attr_value)
                        )
                    )
            else:
                # Add a placeholder value
                match attr_type:
                    case "String":
                        assn_list.append(
                            And(
                                a == attrs[attr_k],
                                d == attr_data_sort.placeholder_str
                            )
                        )
                    case "Boolean":
                        assn_list.append(
                            And(
                                a == attrs[attr_k],
                                d == attr_data_sort.placeholder_bool
                            )
                        )
                    case "Integer":
                        assn_list.append(
                            And(
                                a == attrs[attr_k],
                                d == attr_data_sort.placeholder_int
                            )
                        )
               
        
        if attr_data:
            assn = ForAll(
                [a, d],
                Iff(
                    attr_rel(elems[esn], a, d),
                    Or(*assn_list),
                ),
            )
        else:
            assn = ForAll(
                [a, d],
                Not(attr_rel(elems[esn], a, d))
            )
        # print(assn)
        solver.assert_and_track(assn, f"attribute_values {esn}")

def assert_im_associations(
    assoc_rel: FuncDeclRef,
    solver: Solver,
    im: IntermediateModel, # Contains only bounded elements
    elem: Refs,
    assoc_sort: DatatypeSortRef,
    assoc: Refs,
) -> None:
    """
    ### Effects
    This procedure is effectful on `solver`.
    """

    assoc_ref = Const("a", assoc_sort)
    for (elem_1_k, elem_1_v), elem_2 in product(im.items(), im):
        assn = ForAll(
            [assoc_ref],
            Iff(
                assoc_rel(elem[elem_1_k], assoc_ref, elem[elem_2]),
                Or(
                    *(
                        assoc_ref == assoc[elem_1_assoc_k]
                        for elem_1_assoc_k, elem_1_assoc_elems_k in elem_1_v.associations.items()
                        if elem_2 in elem_1_assoc_elems_k
                    ),
                    solver.ctx
                ),
            ),
        )
        solver.assert_and_track(assn, f"associations {elem_1_k} {elem_2}")


def mk_stringsym_sort_dict(
    im: IntermediateModel,
    mm: MetaModel,
    z3ctx: Context,
    additional_strings: list[str] = []
) -> SortAndRefs:
    strings = (
        {
            v
            for e in im.values()
            for vs in e.attributes.values()
            for v in vs
            if isinstance(v, str)
        }
        | {
            v
            for c in mm.values()
            for a in c.attributes.values()
            if a.default is not None
            for v in a.default
            if isinstance(v, str)
        }
        | {"SCRIPT", "IMAGE"}  # GeneratorKind values
        | {"INGRESS", "EGRESS"} # TODO: Check if this fix is required
        # It solves a KeyError when MC is run on openstack_template.domlx
        | {
            v
            for v in additional_strings
        }
    )
    return mk_stringsym_sort_from_strings(list(strings), z3ctx=z3ctx)

def mk_attr_data_sort(
    str_sort: DatatypeSortRef,
    z3ctx: Context
) -> DatatypeSortRef:
    attr_data = Datatype("AttributeData", ctx=z3ctx)
    attr_data.declare("placeholder_int")
    attr_data.declare("placeholder_bool")
    attr_data.declare("placeholder_str")
    attr_data.declare("int", ("get_int", IntSort(ctx=z3ctx)))
    attr_data.declare("bool", ("get_bool", BoolSort(ctx=z3ctx)))
    attr_data.declare("str", ("get_str", str_sort)) # str_sort is the one returned by the function above
    return attr_data.create()

def mk_stringsym_sort_from_strings(
    strings: list[str],
    z3ctx: Context
) -> SortAndRefs:
    str_list = [f"str_{i}_{symbolize(s)}" for i, s in enumerate(strings)]
    string_sort, str_refs_dict = mk_enum_sort_dict("string", str_list, z3ctx=z3ctx)
    string_sort_dict = {
        s: str_refs_dict[str] for s, str in zip(strings, str_list)
    }
    return string_sort, string_sort_dict

def symbolize(s: str) -> str:
    return "".join([c.lower() if c.isalnum() else "_" for c in s[:16]])
