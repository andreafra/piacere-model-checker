from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name

def concrete_asg_no_vm(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    ielem, concr, provider, celem, asg = Consts("ielem concr provider celem asg", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            concr) == smtenc.classes["concrete_ConcreteInfrastructure"],
        # We don't want the following to happen:
        # If exists ASG(infr) -> VM(infr), then exists a VM(concr) -> VM(infr) 
        And(
            smtenc.element_class_fun(ielem) == smtenc.classes["infrastructure_VirtualMachine"],
            smtenc.association_rel(
                asg, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], ielem),
            (Exists(
                [celem],
                smtenc.association_rel(celem, smtenc.associations["concrete_VirtualMachine::maps"], ielem)
            ))
        )
    )


def ed_concrete_asg_no_vm(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        ielem = Const("ielem", smtsorts.element_sort)
        asg = Const("asg", smtsorts.element_sort)
        ielem_name = get_user_friendly_name(
            intermediate_model, solver.model(), ielem)
        if ielem_name:
            return f"Virtual machine '{ielem_name}' in AutoScale Group '{asg}' should not be present in the concretization layer."
    except:
        return "Any virtual machine in an AutoScale Group should not be present in the concretization layer."

MSG = "All virtual machines in an autoscale group in the infrastructure layer should not be mapped in the concretization layer."

CONCRETE_ASG_NO_VM = (
    concrete_asg_no_vm,
    "concrete_asg_no_vm",
    MSG,
    ed_concrete_asg_no_vm
)