
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
        SECURITY_GROUP_MUST_HAVE_IFACE
    ],
    DOMLVersion.V2_3: [
        VM_HAS_IFACE_V2_3,
        SOFTWARE_PACKAGE_IFACE_NET_V2_3,
        IFACE_UNIQ,
        ALL_SOFTWARE_COMPONENTS_DEPLOYED,
        ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
        ALL_CONCRETE_MAP_SOMETHING,
        SECURITY_GROUP_MUST_HAVE_IFACE
    ],
}

CommonRequirements = {ver: RequirementStore(
    [
        Requirement(
            *rt[:-1], error_description=("BUILTIN", rt[-1]), flipped=True
        ) for rt in reqs
    ])
    for ver, reqs in REQUIREMENTS.items()
}
