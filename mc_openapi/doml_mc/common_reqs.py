
from .imc import Requirement, RequirementStore
from .intermediate_model import DOMLVersion
from .builtin_requirements import *

REQUIREMENTS = {
    DOMLVersion.V2_0: [
        VM_HAS_IFACE,
        SOFTWARE_PACKAGE_IFACE_NET,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE
    ],
    DOMLVersion.V2_1: [
        VM_HAS_IFACE,
        SOFTWARE_PACKAGE_IFACE_NET_V2_1,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE
    ],
    DOMLVersion.V2_2: [
        VM_HAS_IFACE,
        SOFTWARE_PACKAGE_IFACE_NET_V2_1,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE,
        CONCRETE_ASG_NO_VM,
        VM_OS_REQUIRED
    ],
    DOMLVersion.V2_3: [
        VM_HAS_IFACE_V2_3,
        SOFTWARE_PACKAGE_IFACE_NET_V2_3,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE,
        CONCRETE_ASG_NO_VM,
        VM_OS_REQUIRED
    ],
    DOMLVersion.V3_0: [
        VM_HAS_IFACE_V2_3,
        SOFTWARE_PACKAGE_IFACE_NET_V2_3,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE,
        CONCRETE_ASG_NO_VM,
        VM_OS_REQUIRED
    ],
    DOMLVersion.V3_1: [
        VM_HAS_IFACE_V2_3,
        SOFTWARE_PACKAGE_IFACE_NET_V3_1,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED_V3_1,
        ALL_CONCRETE_MAP_SOMETHING_V3_1,
        SECURITY_GROUP_MUST_HAVE_IFACE_V3_1,
        CONCRETE_ASG_NO_VM,
        VM_OS_REQUIRED_V3_1
    ]
}

CommonRequirements = {ver: RequirementStore(
    [
        Requirement(
            *rt[:-1], error_description=("BUILTIN", rt[-1]), flipped=True
        ) for rt in reqs
    ])
    for ver, reqs in REQUIREMENTS.items()
}
