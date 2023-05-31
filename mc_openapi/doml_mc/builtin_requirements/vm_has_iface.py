from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name


def vm_has_iface(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    vm, iface = Consts("vm iface", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            vm) == smtenc.classes["infrastructure_VirtualMachine"],
        Not(
            Exists(
                [iface],
                smtenc.association_rel(
                    vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], iface)
            )
        )
    )

def vm_has_iface_v2_3(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    vm, iface = Consts("vm iface", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            vm) == smtenc.classes["infrastructure_VirtualMachine"],
        Not(
            Exists(
                [iface],
                smtenc.association_rel(
                    vm, smtenc.associations["infrastructure_Node::ifaces"], iface)
            )
        )
    )

def ed_vm_has_iface(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        vm = Const("vm", smtsorts.element_sort)
        vm_name = get_user_friendly_name(
            intermediate_model, solver.model(), vm)
        if vm_name:
            return f"Virtual machine {vm_name} is not connected to any network interface."
    except:
        return "A virtual machine is not connected to any network interface."
    
MSG = "All virtual machines must be connected to at least one network interface."

VM_HAS_IFACE = (
    vm_has_iface, 
    "vm_has_iface",
    MSG,
    ed_vm_has_iface
)

VM_HAS_IFACE_V2_3 = (
    vm_has_iface_v2_3,
    "vm_has_iface",
    MSG,
    ed_vm_has_iface
)