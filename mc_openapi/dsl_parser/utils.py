from mc_openapi.doml_mc.imc import SMTEncoding, SMTSorts
from z3 import Const, DatatypeRef, ExprRef, FuncDeclRef, SortRef

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
        self.curr_vars = set()

        self.curr_index += 1
        return self.curr_index - 1

    def get_free_vars(self, index: int) -> list[ExprRef]:
        vars = self.expressions[index]
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

    def get_element_class(enc: SMTEncoding, const: ExprRef) -> FuncDeclRef:
        return enc.element_class_fun(const)

    def get_class(enc: SMTEncoding, class_name: str) -> DatatypeRef:
        class_name = class_name.replace(".", "_")
        _class = enc.classes.get(class_name, None)
        if _class is not None:
            return _class
        else:
            raise Exception(f"No class named '{class_name}' found.")
            # TODO: Try to suggest the correct class with difflib
            # see: https://docs.python.org/3/library/difflib.html?highlight=get_close_matches#difflib.get_close_matches

    def get_association(enc: SMTEncoding, assoc_name: str) -> DatatypeRef:
        assoc_name = assoc_name.replace(".", "_")
        assoc_name = assoc_name.replace("->", "::")
        assoc = enc.associations.get(assoc_name, None)
        if assoc is not None:
            return assoc
        else:
            raise Exception(f"No association named '{assoc_name}' found.")

    def get_association_rel(enc: SMTEncoding, a: ExprRef, rel: DatatypeRef, b: ExprRef) -> DatatypeRef:
        return enc.association_rel(a, rel, b)

    def get_attribute(enc: SMTEncoding, attr_name: str) -> DatatypeRef:
        attr_name = attr_name.replace(".", "_")
        attr_name = attr_name.replace("->", "::")
        attr = enc.attributes.get(attr_name, None)
        if attr is not None:
            return attr
        else:
            raise Exception(f"No attribute named '{attr_name}' found.")

    def get_attribute_rel(enc: SMTEncoding, a: ExprRef, rel: DatatypeRef, b: ExprRef) -> DatatypeRef:
        return enc.attribute_rel(a, rel, b)

