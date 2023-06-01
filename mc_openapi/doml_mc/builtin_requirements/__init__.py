CELEMS_V2_0 = [
    ("infrastructure_VirtualMachine", "concrete_RuntimeProvider::vms", "concrete_VirtualMachine::maps"),
    ("infrastructure_VMImage", "concrete_RuntimeProvider::vmImages", "concrete_VMImage::maps"),
    ("infrastructure_Network", "concrete_RuntimeProvider::networks", "concrete_Network::maps"),
    ("infrastructure_Storage", "concrete_RuntimeProvider::storages", "concrete_Storage::maps"),
    ("infrastructure_FunctionAsAService", "concrete_RuntimeProvider::faas","concrete_FunctionAsAService::maps"),
    ("infrastructure_ComputingGroup", "concrete_RuntimeProvider::group","concrete_ComputingGroup::maps"),
]

from .vm_has_iface import VM_HAS_IFACE, VM_HAS_IFACE_V2_3
from .software_package_iface_net import SOFTWARE_PACKAGE_IFACE_NET, SOFTWARE_PACKAGE_IFACE_NET_V2_1, SOFTWARE_PACKAGE_IFACE_NET_V2_3
from .iface_uniq import IFACE_UNIQ
from .all_software_components_deployed import ALL_SOFTWARE_COMPONENTS_DEPLOYED
from .all_infrastructure_elements_deployed import ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED
from .all_concrete_maps_something import ALL_CONCRETE_MAP_SOMETHING
from .security_group_must_have_iface import SECURITY_GROUP_MUST_HAVE_IFACE
from .concrete_asg_no_vm import CONCRETE_ASG_NO_VM
from .vm_os_required import VM_OS_REQUIRED

__ALL__ = [
    VM_HAS_IFACE,
    VM_HAS_IFACE_V2_3,
    SOFTWARE_PACKAGE_IFACE_NET,
    SOFTWARE_PACKAGE_IFACE_NET_V2_1,
    SOFTWARE_PACKAGE_IFACE_NET_V2_3,
    IFACE_UNIQ,
    ALL_SOFTWARE_COMPONENTS_DEPLOYED,
    ALL_INFRASTRUCTURE_ELEMENTS_DEPLOYED,
    ALL_CONCRETE_MAP_SOMETHING,
    SECURITY_GROUP_MUST_HAVE_IFACE,
    CONCRETE_ASG_NO_VM,
    VM_OS_REQUIRED
]