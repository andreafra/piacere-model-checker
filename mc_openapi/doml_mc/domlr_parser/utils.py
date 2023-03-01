from difflib import get_close_matches

from mc_openapi.doml_mc.domlr_parser.exceptions import \
    RequirementMissingKeyException
from mc_openapi.doml_mc.imc import SMTEncoding, SMTSorts
from z3 import Const, DatatypeRef, ExprRef, FuncDeclRef, SortRef, Ints, And
from doml_synthesis import State, AssocRel, AttrRel

class StringValuesCache:
    def __init__(self) -> None:
        self.values: set[str] = set()

    def add(self, value: str):
        self.values.add(value)
    
    def get_list(self):
        return list(self.values)

class VarStore:
    """This class provides a way to instance a Z3 variable only the first time
       it's called, and subsequent uses of that variable simply retrieve it
       from the store.
    """

    def __init__(self):
        self.expressions: list[dict[str, bool]] = []
        self.curr_vars: dict[str, bool] = dict()
        self.curr_index: int = 0

    def use(self, name: str):
        self.curr_vars[name] = self.curr_vars.get(name, False)

    def quantify(self, name: str):
        self.curr_vars[name] = True
    
    def get_index_and_push(self):
        self.expressions.append(self.curr_vars)
        self.curr_vars = dict()

        self.curr_index += 1
        return self.curr_index - 1

    def get_free_vars(self, index: int) -> list[ExprRef]:
        vars = self.expressions[index]
        if not vars: 
            return []
        free_vars = [key for key, val in vars.items() if not val]
        return free_vars


class RefHandler:
    """A utility class that provides simplified ways to create Z3 Refs.
    """

    def get_consts(names: list[str], sorts: SMTSorts):
        return [Const(name, sorts.element_sort) for name in names]

    def get_const(name: str, sorts: SMTSorts):
        return Const(name, sorts.element_sort)

    def get_value(name: str, sorts: SMTSorts):
        return Const(name, sorts.attr_data_sort)

    def get_int(value: str, sorts: SMTSorts):
        return sorts.attr_data_sort.int(int(value))

    def get_bool(value: str, sorts: SMTSorts):
        return sorts.attr_data_sort.bool(value == "!True")

    def get_str(value: str, enc: SMTEncoding, sorts: SMTSorts):
        return sorts.attr_data_sort.str(enc.str_symbols[value])

    def get_element_class(enc: SMTEncoding, const: ExprRef) -> FuncDeclRef:
        return enc.element_class_fun(const)

    def get_class(enc: SMTEncoding, class_name: str) -> DatatypeRef:
        class_name = _convert_rel_str(class_name)
        _class = enc.classes.get(class_name, None)
        if _class is not None:
            return _class
        else:
            close_matches = get_close_matches(class_name, enc.classes.keys())
            raise RequirementMissingKeyException("class", class_name, close_matches)

    ASSOCIATION = 0
    ATTRIBUTE = 1

    INTEGER = 2
    BOOLEAN = 3
    STRING = 4

    def get_relationship(enc: SMTEncoding, rel_name: str) -> tuple[DatatypeRef, int]:
        rel_name = _convert_rel_str(rel_name)
        rel = enc.associations.get(rel_name, None)
        if rel is not None:
            return rel, RefHandler.ASSOCIATION
        else:
            rel = enc.attributes.get(rel_name, None)
            if rel is not None:
                return rel, RefHandler.ATTRIBUTE
            else:
                close_matches = get_close_matches(rel_name, list(enc.associations.keys()) + list(enc.attributes.keys()))
                raise RequirementMissingKeyException("relationship", rel_name, close_matches)

    def get_association_rel(enc: SMTEncoding, a: ExprRef, rel: DatatypeRef, b: ExprRef) -> DatatypeRef:
        return enc.association_rel(a, rel, b)

    def get_attribute_rel(enc: SMTEncoding, a: ExprRef, rel: DatatypeRef, b: ExprRef) -> DatatypeRef:
        return enc.attribute_rel(a, rel, b)

class SynthesisRefHandler:
    """A utility class that provides simplified ways to create Z3 Refs.
    To be used when parsing requirements for synthesis
    """

    INTEGER = 2
    BOOLEAN = 3
    STRING = 4

    def get_consts(names: list[str], state: State):
        return [Const(name, state.sorts.Elem) for name in names]

    def get_const(name: str, state: State):
        return Const(name, state.sorts.Elem)

    def get_bool(value: str):
        return value == "!True"

    def get_str(value: str, state: State):
        return state.data.Strings[value]

    def get_element_class(state: State, const: ExprRef) -> FuncDeclRef:
        return state.rels.ElemClass(const)

    def get_class(state: State, class_name: str) -> DatatypeRef:
        class_name = _convert_rel_str(class_name)
        _class = state.data.Classes.get(class_name, None)
        if _class is not None:
            return _class.ref
        else:
            close_matches = get_close_matches(class_name, state.data.Classes.keys())
            raise RequirementMissingKeyException("class", class_name, close_matches)

    def get_assoc(state: State, rel_name: str) -> AssocRel:
        rel_name = _convert_rel_str(rel_name)
        rel = state.data.Assocs.get(rel_name, None)
        if rel is not None:
            return rel
        else: 
            raise f"Association {rel_name} not present in the metamodel!"

    def get_attr(state: State, rel_name: str) -> AttrRel:
            rel_name = _convert_rel_str(rel_name)
            rel = state.data.Attrs.get(rel_name, None)
            if rel is not None:
                return rel
            else: 
                raise f"Attribute {rel_name} not present in the metamodel!"

def _convert_rel_str(rel: str) -> str:
    tokens = rel.replace("abstract", "infrastructure").split(".") 
    if len(tokens) == 2:
        return tokens[0] + "_" + tokens[1]
    if len(tokens) == 3:
        return tokens[0] + "_" + tokens[1] + "::" + tokens[2]
    raise f"Bad relationship name: {rel}"
