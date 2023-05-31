from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name

# There are no duplicated interfaces.
def iface_uniq(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    endPointAttr = smtenc.attributes["infrastructure_NetworkInterface::endPoint"]
    ni1, ni2 = Consts("ni1 ni2", smtsorts.element_sort)
    value = Const("value", smtsorts.attr_data_sort)
    return And(
        smtenc.attribute_rel(ni1, endPointAttr, value),
        smtenc.attribute_rel(ni2, endPointAttr, value),
        ni1 != ni2,
    )

def ed_iface_uniq(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        ni1, ni2 = Consts("ni1 ni2", smtsorts.element_sort)
        model = solver.model()
        ni1_name = get_user_friendly_name(intermediate_model, model, ni1)
        ni2_name = get_user_friendly_name(intermediate_model, model, ni2)
        if ni1_name and ni2_name:
            return f"Network interfaces '{ni1_name}' and '{ni2_name}' share the same IP address."
    except:
        return "Two network interfaces share the same IP address."

MSG = "There are no duplicated interfaces."

IFACE_UNIQ = (
    iface_uniq,
    "iface_uniq",
    MSG,
    ed_iface_uniq
)