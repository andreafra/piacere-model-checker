# vm, iface = get_consts(smtsorts, ["vm", "iface"])
# return And(
#     smtenc.element_class_fun(vm) == smtenc.classes["infrastructure_VirtualMachine"],
#     Not(
#         Exists(
#             [iface],
#             ENCODINGS.association_rel(vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], iface)
#         )
#     )
# )

+   "All VMs have at least 512 MB of memory"
    forall vm (
        vm is class infrastructure.VirtualMachine
        implies
        (
            vm has abstract.ComputingNode.memory_mb Mem
            and
            Mem < 512
        )
    )
    
    ---
    "All VMs have at least 256 MB of memory"
