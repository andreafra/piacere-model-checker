from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name

# From DOML V2.3+:
# The association between security groups and network interfaces can now be done only
# in the security groups definition through the “ifaces” keyword (removed the "security"
# keyword in the network interface definition)
def security_group_must_have_iface(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    sg, iface = Consts("sg iface", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            sg) == smtenc.classes["infrastructure_SecurityGroup"],
        Not(Exists([iface],
            smtenc.association_rel(
                iface, smtenc.associations["infrastructure_NetworkInterface::associated"], sg)
        ))
    )

def ed_security_group_must_have_iface(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        sg = Const("sg", smtsorts.element_sort)
        sg_name = get_user_friendly_name(
            intermediate_model, solver.model(), sg)
        if sg_name:
            return f"Security group '{sg_name}' is not associated with any network interface."
    except:
        return "A network interface doesn't belong to any security group, or a security group is not associated with any network interface."

MSG = "All security group should be a associated to a network interface."

SECURITY_GROUP_MUST_HAVE_IFACE = (
    security_group_must_have_iface,
    "security_group_must_have_iface",
    MSG,
    ed_security_group_must_have_iface
)