import logging
from mc_openapi.doml_mc.intermediate_model import DOMLElement
from mc_openapi.doml_mc.mc import ModelChecker
from ipaddress import IPv4Address, IPv4Network


BASE_ADDR = '0.0.0.0'


CONCRETE_NETWORK = 'concrete_Network'
# associations
ASSOC_SUBNETS = 'infrastructure_Network::subnets'
ASSOC_CONCRETE_SUBNETS = 'concrete_Network::subnets'
ASSOC_CONCRETE_MAPS = 'concrete_Network::maps'
ASSOC_GATEWAYS = 'infrastructure_Network::gateways'
ASSOC_NETIFACE = 'infrastructure_Network::connectedIfaces'

# attributes
ATTR_NET_CIDR = 'infrastructure_Network::cidr'
ATTR_GATEWAY_ADDRESS = 'infrastructure_InternetGateway::address'
ATTR_NETIFACE_ADDRESS = 'infrastructure_NetworkInterface::endPoint'
ATTR_PROTOCOL = 'infrastructure_Network::protocol'
ATTR_CONCRETE_PROTOCOL = 'concrete_Network::protocol'
ATTR_CONCRETE_ADDRESS_RANGE = 'concrete_Network::addressRange'

def validate_network_address(imc: ModelChecker):
    """
    HOW IT WORKS:

    * Infrastructure Layer
        - [n] Network.protocol
        - [e] InternetGateway.address
        - [e] NetworkInterface.endPoint
    * Concrete Layer
        - [n] Network.protocol
        - [n] Network.addressRange
        - [n] Subnet.addressRange

    before MC
    validate network
    generate report
    attach report to HTML output
    """
    im = imc.intermediate_model

    # warnings: list[str] = []
    warnings: list[str] = []

    ## Helpers ##
    def get_attr(elem: DOMLElement, attr_id: str):
        if elem := elem.attributes.get(attr_id):
            return elem[0]
        return None
        
    def get_assocs(elem: DOMLElement, assoc_id: str):
        return elem.associations.get(assoc_id, [])

    def get_elem(elem: DOMLElement, assoc_id: str):
        assocs = list(get_assocs(elem, assoc_id))
        if len(assocs) >= 1:
            return im.get(assocs[0])
        return None

    def validate_net(cnet: DOMLElement, parent_net: DOMLElement | None = None):
        
        if (parent_net):
            check_proper_subnet(cnet, parent_net)
            
        if inet := get_elem(cnet, ASSOC_CONCRETE_MAPS):
            check_infr_and_conc_protocol_match(inet, cnet)
            check_cidr_and_address_range(inet, cnet)
            check_gateway_belongs_to_network(inet, cnet)
            check_iface_belongs_to_network(inet, cnet)

        debug =  f"{cnet.user_friendly_name} [concrete]\n"
        debug += f"\tprotocol={get_attr(cnet, ATTR_CONCRETE_PROTOCOL)}\n"
        debug += f"\taddress_range={get_attr(cnet, ATTR_CONCRETE_ADDRESS_RANGE)}\n"
        debug += f"\tsubnets=\t{get_assocs(cnet, ASSOC_CONCRETE_SUBNETS)}\n"
        if inet:
            debug += f"{inet.user_friendly_name} [infrastructure]\n"
            debug += f"\tprotocol={get_attr(inet, ATTR_PROTOCOL)}\n"
            debug += f"\tcidr={get_attr(inet, ATTR_NET_CIDR)}\n"
            debug += f"\tsubnets=\t{get_assocs(inet, ASSOC_SUBNETS)}\n"
            debug += f"\tifaces=\t{get_assocs(inet, ASSOC_NETIFACE)}\n"
            debug += f"\tgateways=\t{get_assocs(inet, ASSOC_GATEWAYS)}\n"
        debug += "\n"
        # print(debug)

        csubnet_ids = get_assocs(cnet, ASSOC_CONCRETE_SUBNETS)
        for csubnet_id in csubnet_ids:
            if csubnet := im.get(csubnet_id):

                validate_net(csubnet, cnet)

    ## Checks ##
    def check_infr_and_conc_protocol_match(inet: DOMLElement, cnet: DOMLElement):
        """Checks if the protocol of an infrastructure network matches the respective protocol of its concrete counterpart."""
        iprot = get_attr(inet, ATTR_PROTOCOL)
        cprot = get_attr(cnet, ATTR_CONCRETE_PROTOCOL)
        if iprot and cprot and iprot != cprot:
            warnings.append(f"Protocol of infrastructure network '{inet.user_friendly_name}' must match protocol of concrete network '{cnet.user_friendly_name}'.")

    def check_cidr_and_address_range(inet: DOMLElement, cnet: DOMLElement, warnings=warnings):
        """Checks if the addressRange of a concrete network respects the CIDR specified in the infrastructure layer."""
        cidr = get_attr(inet, ATTR_NET_CIDR)
        addr_range = get_attr(cnet, ATTR_CONCRETE_ADDRESS_RANGE)
        if cidr and addr_range:
            try:
                addr_range = IPv4Network(addr_range)
                if addr_range.prefixlen != cidr:
                    warnings.append(f"CIDR ({cidr}) of infrastructure network '{inet.user_friendly_name}' does not match the address range of concrete network '{cnet.user_friendly_name}'.")
            except:
                warnings.append(f"Failed to parse concrete network '{cnet.user_friendly_name}' address range as an IPv4Network.")
            
    def check_proper_subnet(cnet: DOMLElement, parent_net: DOMLElement):
        """Checks if a subnet address range respects the parent net."""
        addr_range = get_attr(cnet, ATTR_CONCRETE_ADDRESS_RANGE)
        parent_addr_range = get_attr(parent_net, ATTR_CONCRETE_ADDRESS_RANGE)
        if addr_range and parent_addr_range:
            try: 
                addr_range = IPv4Network(addr_range)
                parent_addr_range = IPv4Network(parent_addr_range)

                if not addr_range.subnet_of(parent_addr_range):
                    warnings.append(f"Subnet '{cnet.user_friendly_name}' is not a proper subnet of '{parent_net.user_friendly_name}'.")
            except:
                warnings.append(f"Failed to parse concrete network '{cnet.user_friendly_name}' or '{parent_net.user_friendly_name}' address range as an IPv4Network.")

    def check_gateway_belongs_to_network(inet: DOMLElement, cnet: DOMLElement):
        """Checks if the address of the gateways of a network belongs to that network address range."""
        addr_range = get_attr(cnet, ATTR_CONCRETE_ADDRESS_RANGE)
        gateway_ids = get_assocs(inet, ASSOC_GATEWAYS)

        if addr_range and gateway_ids:
            for gateway_id in gateway_ids:
                if gateway := im.get(gateway_id):
                    addr_gateway = get_attr(gateway, ATTR_GATEWAY_ADDRESS)
                    if addr_gateway:
                        try:
                            addr_range = IPv4Network(addr_range)
                            addr_gateway = IPv4Address(addr_gateway)
                            if addr_gateway not in addr_range:
                                warnings.append(f"Gateway '{gateway.user_friendly_name}' does not belong to network '{cnet.user_friendly_name}'.")
                        except:
                            warnings.append(f"Failed to parse concrete network {cnet.user_friendly_name} address range or its gateway address.")

    def check_iface_belongs_to_network(inet: DOMLElement, cnet: DOMLElement):
        """Checks if the address of the network interfaces of a network belongs to that network address range."""
        addr_range = get_attr(cnet, ATTR_CONCRETE_ADDRESS_RANGE)
        iface_ids = get_assocs(inet, ASSOC_NETIFACE)

        if addr_range and iface_ids:
            for iface_id in iface_ids:
                if iface := im.get(iface_id):
                    addr_iface = get_attr(iface, ATTR_NETIFACE_ADDRESS)
                    if addr_iface:
                        try:
                            addr_range = IPv4Network(addr_range)
                            addr_iface = IPv4Address(addr_iface)
                            if addr_iface not in addr_range:
                                warnings.append(f"Network Interface '{addr_iface.user_friendly_name}' does not belong to network '{cnet.user_friendly_name}'.")
                        except Exception as e:
                            print(e)
                            warnings.append(f"Failed to parse concrete network {cnet.user_friendly_name} address range or its associated network interface '{iface.user_friendly_name}' address.")




    concrete_networks = [e for e in im.values() if e.class_ == CONCRETE_NETWORK]

    # print('-'*20)
    # print('[DEBUG] Network Validation')

    for cnet in concrete_networks:
        validate_net(cnet)
               
    # print('-'*20)
    # print(warnings)
    # print('-'*20)

    # networks = [e for e in im.values() if e.class_ == 'concrete_Network']
    # subnets = [e for e in im.values() if e.class_ == 'infrastructure_Subnet']
    # ifaces = [e for e in im.values() if e.class_ == 'infrastructure_NetworkInterface']


    # def visit_subnet(net: DOMLElement, acc: list):
    #     """Recursively navigate subnets to populate the `acc` list with all the subnet in a network."""
    #     for subnet in get_assocs(net, ASSOC_SUBNETS):
    #         subnet = im[subnet]
    #         subnet_addr = fix_invalid_address(get_attr(subnet, ATTR_NET_ADDRESS), net, warnings)
    #         acc.append((subnet, IPv4Network(subnet_addr)))
    #         visit_subnet(subnet, acc)

    # def fix_invalid_address(address: any, net: DOMLElement, warning: list):
    #     # TODO: Use a match statement or use regexps once syntax for CIDR/Address is clear
    #     if isinstance(address, str) and address.startswith('/'):
    #         warning.append(("Network", f"Net '{net.user_friendly_name}' has an incomplete address: '{address}'. '0.0.0.0' has been temporarily assigned."))
    #         return f"{BASE_ADDR}{address}"

    #     return address


    # for network in networks:

    #     warning = []

    #     # Tuple(elem, cidr)
    #     subnets: list[tuple[DOMLElement, IPv4Network]] = []
    #     # Tuple(elem, address)
    #     addresses: list[tuple[DOMLElement, IPv4Address]] = []

    #     # Add subnets (Networks)
    #     visit_subnet(network, subnets)

    #     # pprint("SUBNETS:")
    #     # pprint(subnets)

    #     # Add addresses (gateways, ifaces)
    #     for gateway in get_assocs(network, ASSOC_GATEWAYS):
    #         gateway = im[gateway]
    #         if gateway_address := get_attr(gateway, ATTR_GATEWAY_ADDRESS):
    #             addresses.append((gateway, IPv4Address(gateway_address)))

    #     for iface in ifaces:
    #         if owner_id := get_assocs(iface, ASSOC_IFACE_NET):
    #             owner = im[list(owner_id)[0]]
    #             if owner.id_ in [s.id_ for (s, _) in subnets] + [network.id_]:
    #                 if ((iface_address := get_attr(iface, ATTR_NETIFACE_ADDRESS))
    #                 and (owner_address := get_attr(owner, ATTR_NET_ADDRESS))):
    #                     owner_address = fix_invalid_address(owner_address, owner, warning)
    #                     iface_address = IPv4Address(iface_address)
    #                     owner_address = IPv4Network(owner_address)
    #                     # TODO: Remove?
    #                     logging.info(f"{iface.user_friendly_name} ({iface_address}) belongs to {owner.user_friendly_name} ({owner_address})? {iface_address in owner_address.hosts()}")

    #                     addresses.append((iface, iface_address))
    #             else:
    #                 logging.info(f"NetworkInterface '{iface.user_friendly_name}' does not belong to net '{owner.user_friendly_name}'.")
    #                 warning.append((
    #                     "Address", f"NetworkInterface '{iface.user_friendly_name}' does not belong to net '{owner.user_friendly_name}'."
    #                 ))

    #     # Validate Network and Subnets
    #     net_addr = fix_invalid_address(get_attr(network, ATTR_NET_ADDRESS), network, warning)
    #     # prepend 0.0.0.0 if starts with / i guess, print a warning
    #     print(f"{net_addr}\t{network.user_friendly_name}")

    #     net = IPv4Network(net_addr)

    #     if len(subnets) > 0:
    #         for (obj, sn) in subnets:
    #             logging.info(f"{sn}\t{obj.user_friendly_name} belongs? {sn.subnet_of(net)}")
    #             if not sn.subnet_of(net):
    #                 warning.append((
    #                     "Subnet", f"Subnet {obj.user_friendly_name} ({sn}) does not belong to net '{network.user_friendly_name}' ({net_addr})."
    #                 ))
    #     else:
    #         print("No subnets found!")

    #     # Validate addresses (again)
    #     for (obj, addr) in addresses:
    #         if addr not in net.hosts():
    #             warning.append((
    #                 "Address", f"'{obj.user_friendly_name}' [{obj.class_}] ({addr}) does not belong to net '{network.user_friendly_name}' ({net_addr})."
    #             ))
    #         logging.info(f"NetworkInterface '{obj.user_friendly_name}' ({addr}) belong to net '{network.user_friendly_name}' ({net_addr})? {addr in net.hosts()}")

    #     warnings.append((network.user_friendly_name, list(set(warning))))

    return warnings
        
    

  

