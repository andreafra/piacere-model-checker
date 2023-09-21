from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name


def vm_os_required(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    vm, cont, ccfg = Consts("vm cont ccfg", smtsorts.element_sort)
    os = Const("os", smtsorts.attr_data_sort)
    return And(
        smtenc.element_class_fun(
            vm) == smtenc.classes["infrastructure_VirtualMachine"],
        smtenc.element_class_fun(
            cont) == smtenc.classes["infrastructure_Container"],
        Not(
            Exists(
                [vm, os, ccfg],
                And(
                    smtenc.association_rel(
                        cont, smtenc.associations["infrastructure_Container::configs"], ccfg),
                    smtenc.association_rel(
                        ccfg, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                    smtenc.attribute_rel(
                        vm, smtenc.attributes["infrastructure_ComputingNode::os"], os)
                )
            )
        )
    )

def vm_os_required_v3_1(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    vm, cont, ccfg = Consts("vm cont ccfg", smtsorts.element_sort)
    os = Const("os", smtsorts.attr_data_sort)
    return And(
        smtenc.element_class_fun(
            vm) == smtenc.classes["infrastructure_VirtualMachine"],
        smtenc.element_class_fun(
            cont) == smtenc.classes["infrastructure_Container"],
        Not(
            Exists(
                [vm, os, ccfg],
                And(
                    smtenc.association_rel(
                        cont, smtenc.associations["infrastructure_Container::hostConfigs"], ccfg),
                    smtenc.association_rel(
                        ccfg, smtenc.associations["infrastructure_ContainerHostConfig::host"], vm),
                    smtenc.attribute_rel(
                        vm, smtenc.attributes["infrastructure_ComputingNode::os"], os)
                )
            )
        )
    )

def ed_vm_os_required(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        cont = Const("cont", smtsorts.element_sort)
        vm = Const("vm", smtsorts.element_sort)
        cont_name = get_user_friendly_name(
            intermediate_model, solver.model(), cont)
        vm_name = get_user_friendly_name(
            intermediate_model, solver.model(), vm)
        if cont_name and vm_name:
            return f"The virtual machine '{vm_name}' hosting container '{cont_name}' needs an OS."
    except:
        return "A Virtual machine hosting a container needs an OS."
    

MSG = "When something is hosted on a virtual machine (e.g.: containers), the VM must have the 'os' specified."

VM_OS_REQUIRED = (
    vm_os_required, 
    "vm_os_required",
    MSG,
    ed_vm_os_required
)

VM_OS_REQUIRED_V3_1 = (
    vm_os_required_v3_1, 
    "vm_os_required",
    MSG,
    ed_vm_os_required
)