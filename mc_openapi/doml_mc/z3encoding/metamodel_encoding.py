from z3 import (
    BoolSort,
    Context,
    DatatypeSortRef,
    FuncDeclRef,
    Function,
    EnumSort
)
from ..intermediate_model import MetaModel

from .types import SortAndRefs

def mk_class_sort_dict(mm: MetaModel, z3ctx: Context) -> SortAndRefs:
    return mk_enum_sort_dict("Class", list(mm), z3ctx)


def mk_attribute_sort_dict(
    mm: MetaModel,
    z3ctx: Context
) -> SortAndRefs:
    atts = [
        f"{cname}::{aname}"
        for cname, c in mm.items()
        for aname in c.attributes
    ]
    return mk_enum_sort_dict("Attribute", atts, z3ctx)


def mk_association_sort_dict(
    mm: MetaModel,
    z3ctx: Context
) -> SortAndRefs:
    assocs = [
        f"{cname}::{aname}"
        for cname, c in mm.items()
        for aname in c.associations
    ]
    return mk_enum_sort_dict("Association", assocs, z3ctx)

def mk_enum_sort_dict(name: str, values: list[str], z3ctx: Context) -> SortAndRefs:
    """Makes a Z3 sort and a dict indexing sort values by their name"""

    sort, datatype_refs = EnumSort(name, values, ctx=z3ctx)
    return sort, dict(zip(values, datatype_refs))

def def_attribute_rel(
    attr_sort: DatatypeSortRef,
    elem_sort: DatatypeSortRef,
    attr_data_sort: DatatypeSortRef
) -> FuncDeclRef:
    return Function("attribute", elem_sort, attr_sort, attr_data_sort, BoolSort(ctx=elem_sort.ctx))


def def_association_rel(
    assoc_sort: DatatypeSortRef,
    elem_sort: DatatypeSortRef
) -> FuncDeclRef:
    return Function("association", elem_sort, assoc_sort, elem_sort, BoolSort(ctx=elem_sort.ctx))
