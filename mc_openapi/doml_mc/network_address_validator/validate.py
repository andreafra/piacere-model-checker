import logging
from mc_openapi.doml_mc.intermediate_model import DOMLElement
from mc_openapi.doml_mc.mc import ModelChecker
from ipaddress import IPv4Address, IPv4Network


BASE_ADDR = '0.0.0.0'

ASSOC_SUBNETS = 'infrastructure_Network::subnets'
ASSOC_GATEWAYS = 'infrastructure_Network::gateways'
ASSOC_IFACE_NET = 'infrastructure_NetworkInterface::belongsTo'

ATTR_NET_ADDRESS = 'infrastructure_Network::addressRange'
ATTR_GATEWAY_ADDRESS = 'infrastructure_InternetGateway::address'
ATTR_IFACE_ADDRESS = 'infrastructure_NetworkInterface::endPoint'

def get_attr(elem: DOMLElement, attr_id: str):
    if elem := elem.attributes.get(attr_id):
        return elem[0]
    return None
    
def get_assocs(elem: DOMLElement, assoc_id: str):
    return elem.associations.get(assoc_id, [])

def validate_network_address(imc: ModelChecker):
    """
    HOW IT WORKS:

    - Network.addressRange
    - Subnet.addressRange
    - InternetGateway.address
    - NetworkInterface.endPoint

    before MC
    validate network
    generate report
    attach report to HTML output
    """

    im = imc.intermediate_model

    networks = [e for e in im.values() if e.class_ == 'infrastructure_Network']
    ifaces = [e for e in im.values() if e.class_ == 'infrastructure_NetworkInterface']
    subnets = [e for e in im.values() if e.class_ == 'infrastructure_Subnet']

    def visit_subnet(net: DOMLElement, acc: list):
        """Recursively navigate subnets to populate the `acc` list with all the subnet in a network."""
        for subnet in get_assocs(net, ASSOC_SUBNETS):
            subnet = im[subnet]
            subnet_addr = fix_invalid_address( get_attr(subnet, ATTR_NET_ADDRESS) )
            acc.append((subnet, IPv4Network(subnet_addr)))
            visit_subnet(subnet, acc)

    def fix_invalid_address(address: any, net: DOMLElement, warning: list):
        # TODO: Use a match statement or use regexps once syntax for CIDR/Address is clear
        if isinstance(address, str) and address.startswith('/'):
            warning.append(("Network", f"Net '{net.user_friendly_name}' has an incomplete address: '{address}'. '0.0.0.0' has been temporarily assigned."))
            return f"{BASE_ADDR}{address}"

        return address

    warnings: list[tuple[str, list[tuple[str, str]]]] = []

    for network in networks:

        warning = []

        # Tuple(elem, cidr)
        subnets: list[tuple[DOMLElement, IPv4Network]] = []
        # Tuple(elem, address)
        addresses: list[tuple[DOMLElement, IPv4Address]] = []

        # Add subnets (Networks)
        visit_subnet(network, subnets)

        # pprint("SUBNETS:")
        # pprint(subnets)

        # Add addresses (gateways, ifaces)
        for gateway in get_assocs(network, ASSOC_GATEWAYS):
            gateway = im[gateway]
            if gateway_address := get_attr(gateway, ATTR_GATEWAY_ADDRESS):
                addresses.append((gateway, IPv4Address(gateway_address)))

        for iface in ifaces:
            if owner_id := get_assocs(iface, ASSOC_IFACE_NET):
                owner = im[list(owner_id)[0]]
                if owner.id_ in [s.id_ for (s, _) in subnets] + [network.id_]:
                    if ((iface_address := get_attr(iface, ATTR_IFACE_ADDRESS))
                    and (owner_address := get_attr(owner, ATTR_NET_ADDRESS))):
                        owner_address = fix_invalid_address(owner_address, owner, warning)
                        iface_address = IPv4Address(iface_address)
                        owner_address = IPv4Network(owner_address)
                        # TODO: Remove?
                        logging.info(f"{iface.user_friendly_name} ({iface_address}) belongs to {owner.user_friendly_name} ({owner_address})? {iface_address in owner_address.hosts()}")

                        addresses.append((iface, iface_address))
                else:
                    logging.info(f"NetworkInterface '{iface.user_friendly_name}' does not belong to net '{owner.user_friendly_name}'.")
                    warning.append((
                        "Address", f"NetworkInterface '{iface.user_friendly_name}' does not belong to net '{owner.user_friendly_name}'."
                    ))

        # Validate Network and Subnets
        net_addr = fix_invalid_address(get_attr(network, ATTR_NET_ADDRESS), network, warning)
        # prepend 0.0.0.0 if starts with / i guess, print a warning
        print(f"{net_addr}\t{network.user_friendly_name}")

        net = IPv4Network(net_addr)

        if len(subnets) > 0:
            for (obj, sn) in subnets:
                logging.info(f"{sn}\t{obj.user_friendly_name} belongs? {sn.subnet_of(net)}")
                if not sn.subnet_of(net):
                    warning.append((
                        "Subnet", f"Subnet {obj.user_friendly_name} ({sn}) does not belong to net '{network.user_friendly_name}' ({net_addr})."
                    ))
        else:
            print("No subnets found!")

        # Validate addresses (again)
        for (obj, addr) in addresses:
            if addr not in net.hosts():
                warning.append((
                    "Address", f"'{obj.user_friendly_name}' [{obj.class_}] ({addr}) does not belong to net '{network.user_friendly_name}' ({net_addr})."
                ))
            logging.info(f"NetworkInterface '{obj.user_friendly_name}' ({addr}) belong to net '{network.user_friendly_name}' ({net_addr})? {addr in net.hosts()}")

        warnings.append((network.user_friendly_name, list(set(warning))))

    return warnings
        
    

  

