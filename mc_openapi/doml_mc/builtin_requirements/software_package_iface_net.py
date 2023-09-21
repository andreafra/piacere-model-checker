from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name

# All software packages can see the interfaces they need through a common network.

def software_package_iface_net(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    asc_consumer, asc_exposer, siface, net, net_iface, cnode, cdeployment, enode, edeployment, vm, csubnet, esubnet = Consts(
        "asc_consumer asc_exposer siface net net_iface cnode cdeployment enode edeployment vm csubnet esubnet", smtsorts.element_sort
    )
    return And(
        smtenc.association_rel(
            asc_consumer, smtenc.associations["application_SoftwareComponent::exposedInterfaces"], siface),
        smtenc.association_rel(
            asc_exposer, smtenc.associations["application_SoftwareComponent::consumedInterfaces"], siface),
        Not(
            Or(
                Exists(
                    [cdeployment, cnode, edeployment, enode, net],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Exists(
                            [vm, net_iface],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::hosts"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    # ASC_EXPLORER > CN > IFACE > NET
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    # ASC_EXPOSER > CONTAINER > CN > IFACE > NET
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::hosts"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    # ASC_EXPLORER > ASG > CN > IFACE > NET
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        )
                    )
                ),  #  OR
                Exists(
                    [cdeployment, cnode, edeployment, enode, csubnet, esubnet],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Or(
                            smtenc.association_rel(
                                csubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], esubnet),
                            smtenc.association_rel(
                                esubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], csubnet),
                        ),
                        Exists(
                            [vm, net_iface],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    # ASC_CONSUMER > CN > IFACE > csubnet
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    # ASC_CONSUMER > CONTAINER > CN > IFACE > csubnet
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::hosts"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    # ASC_CONSUMER > ASG > CN > IFACE > csubnet
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    # ASC_EXPOSER > CN > IFACE > esubnet
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    # ASC_EXPOSER > CONTAINER > CN > IFACE > esubnet
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::hosts"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    # ASC_EXPLORER > ASG > CN > IFACE > esubnet
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def software_package_iface_net_v2_1(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    asc_consumer, asc_exposer, siface, net, net_iface, cnode, cdeployment, enode, edeployment, vm, cconf, csubnet, esubnet = Consts(
        "asc_consumer asc_exposer siface net net_iface cnode cdeployment enode edeployment vm cconf csubnet esubnet", smtsorts.element_sort
    )
    return And(
        smtenc.association_rel(
            asc_consumer, smtenc.associations["application_SoftwareComponent::exposedInterfaces"], siface),
        smtenc.association_rel(
            asc_exposer, smtenc.associations["application_SoftwareComponent::consumedInterfaces"], siface),
        Not(
            Or(
                Exists(
                    [cdeployment, cnode, edeployment, enode, net],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        )
                    )
                ),  # OR
                Exists(
                    [cdeployment, cnode, edeployment, enode, csubnet, esubnet],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Or(
                            smtenc.association_rel(
                                csubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], esubnet),
                            smtenc.association_rel(
                                esubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], csubnet),
                        ),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_ComputingNode::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def software_package_iface_net_v2_3(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    asc_consumer, asc_exposer, siface, net, net_iface, cnode, cdeployment, enode, edeployment, vm, cconf, csubnet, esubnet = Consts(
        "asc_consumer asc_exposer siface net net_iface cnode cdeployment enode edeployment vm cconf csubnet esubnet", smtsorts.element_sort
    )
    return And(
        smtenc.association_rel(
            asc_consumer, smtenc.associations["application_SoftwareComponent::exposedInterfaces"], siface),
        smtenc.association_rel(
            asc_exposer, smtenc.associations["application_SoftwareComponent::consumedInterfaces"], siface),
        Not(
            Or(
                Exists(
                    [cdeployment, cnode, edeployment, enode, net],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        )
                    )
                ),  # OR
                Exists(
                    [cdeployment, cnode, edeployment, enode, csubnet, esubnet],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Or(
                            smtenc.association_rel(
                                csubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], esubnet),
                            smtenc.association_rel(
                                esubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], csubnet),
                        ),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::configs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                )
                            )
                        )
                    )
                )
            )
        )
    )

def software_package_iface_net_v3_1(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    asc_consumer, asc_exposer, siface, net, net_iface, cnode, cdeployment, enode, edeployment, vm, cconf, csubnet, esubnet = Consts(
        "asc_consumer asc_exposer siface net net_iface cnode cdeployment enode edeployment vm cconf csubnet esubnet", smtsorts.element_sort
    )
    return And(
        smtenc.association_rel(
            asc_consumer, smtenc.associations["application_SoftwareComponent::exposedInterfaces"], siface),
        smtenc.association_rel(
            asc_exposer, smtenc.associations["application_SoftwareComponent::consumedInterfaces"], siface),
        Not(
            Or(
                Exists(
                    [cdeployment, cnode, edeployment, enode, net],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::hostConfigs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerHostConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::hostConfigs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerHostConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], net),
                                ),
                            )
                        )
                    )
                ),  # OR
                Exists(
                    [cdeployment, cnode, edeployment, enode, csubnet, esubnet],
                    And(
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::component"], asc_consumer),
                        smtenc.association_rel(
                            cdeployment, smtenc.associations["commons_Deployment::node"], cnode),
                        Or(
                            smtenc.association_rel(
                                csubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], esubnet),
                            smtenc.association_rel(
                                esubnet, smtenc.associations["infrastructure_Subnet::connectedTo"], csubnet),
                        ),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_consumer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a container hosted in a VM with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_Container::hostConfigs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerHostConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                                And(  # asc_consumer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        cnode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], csubnet),
                                ),
                            )
                        ),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::component"], asc_exposer),
                        smtenc.association_rel(
                            edeployment, smtenc.associations["commons_Deployment::node"], enode),
                        Exists(
                            [vm, net_iface, cconf],
                            Or(
                                And(  # asc_exposer is deployed on a component with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a container hosted on a VM with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_Container::hostConfigs"], cconf),
                                    smtenc.association_rel(
                                        cconf, smtenc.associations["infrastructure_ContainerHostConfig::host"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                ),
                                And(  # asc_exposer is deployed on a VM in an AutoScalingGroup with an interface in network n
                                    smtenc.association_rel(
                                        enode, smtenc.associations["infrastructure_AutoScalingGroup::machineDefinition"], vm),
                                    smtenc.association_rel(
                                        vm, smtenc.associations["infrastructure_Node::ifaces"], net_iface),
                                    smtenc.association_rel(
                                        net_iface, smtenc.associations["infrastructure_NetworkInterface::belongsTo"], esubnet),
                                )
                            )
                        )
                    )
                )
            )
        )
    )


def ed_software_package_iface_net(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        asc_consumer, asc_exposer, siface = Consts(
            "asc_consumer asc_exposer siface", smtsorts.element_sort
        )
        model = solver.model()
        asc_consumer_name = get_user_friendly_name(
            intermediate_model, model, asc_consumer)
        asc_exposer_name = get_user_friendly_name(
            intermediate_model, model, asc_exposer)
        siface_name = get_user_friendly_name(intermediate_model, model, siface)
        if asc_consumer_name and asc_exposer_name and siface_name:
            return (
                f"Software components '{asc_consumer_name}' and '{asc_exposer_name}' "
                f"are supposed to communicate through interface '{siface_name}', "
                "but they are deployed to nodes that cannot communicate through a common network."
            )
    except:
        return "A software package is deployed on a node that has no access to an interface it consumes."
    
MSG = "All software packages can see the interfaces they need through a common network."

SOFTWARE_PACKAGE_IFACE_NET = (
    software_package_iface_net, 
    "software_package_iface_net",
    MSG,
    ed_software_package_iface_net
)

SOFTWARE_PACKAGE_IFACE_NET_V2_1 = (
    software_package_iface_net_v2_1, 
    "software_package_iface_net",
    MSG,
    ed_software_package_iface_net
)

SOFTWARE_PACKAGE_IFACE_NET_V2_3 = (
    software_package_iface_net_v2_3,
    "software_package_iface_net",
    MSG,
    ed_software_package_iface_net
)

SOFTWARE_PACKAGE_IFACE_NET_V3_1 = (
    software_package_iface_net_v3_1,
    "software_package_iface_net",
    MSG,
    ed_software_package_iface_net
)