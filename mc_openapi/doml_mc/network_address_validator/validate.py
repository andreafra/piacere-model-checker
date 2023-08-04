from mc_openapi.doml_mc.intermediate_model.doml_element import DOMLElement
from mc_openapi.doml_mc.mc import ModelChecker
import ipaddress

def validate_network_address(imc: ModelChecker):
    """
    HOW IT WORKS:

    - Network.cidr
    - Subnet.cidr
    - InternetGateway.address
    - NetworkInterface.endPoint
    """

    im = imc.intermediate_model

    networks = [e for e in im.values() if e.class_ == 'infrastructure_Network']
    ifaces = [e for e in im.values() if e.class_ == 'infrastructure_NetworkInterface']

    addresses = set()

    def get_attr(elem: DOMLElement, attr_id: str):
        if elem := elem.attributes.get(attr_id):
            return elem[0]
    def get_assocs(elem: DOMLElement, assoc_id: str):
        return elem.associations.get(assoc_id, [])

    NETS = {}

    # We can have multiple networks. For each of them, retrieve:
    # - CIDR (/XX)
    # - The base address(es): we can get them from the gateway address + the CIDR
    for network in networks:

        net_cidr = get_attr(network, 'infrastructure_Network::cidr')

        net = Network(("0.0.0.0", net_cidr))
        
        gateways = get_assocs(network, 'infrastructure_Network::gateways')
        for gateway_id in gateways:
            gateway = im[gateway_id]
            gateway_address = get_attr(gateway, 'infrastructure_InternetGateway::address')
            
            net.net.network_address = ipaddress.IPv4Network((gateway_address, net_cidr), strict=False).network_address

            net.add_address(gateway_address)

        subnets = get_assocs(network, 'infrastructure_Network::subnets')
        for subnet_id in subnets:
            subnet = im[subnet_id]
            subnet_cidr = get_attr(subnet, 'infrastructure_Network::cidr')
            
            net.add_subnet(subnet_cidr)
        
        print(net.net)
        print(net.subnets)
        print(net.addresses)
        NETS[network.user_friendly_name] = net
    
    for iface in ifaces:
        print(iface)
        net_ids = get_assocs(iface, 'infrastructure_NetworkInterface::belongsTo')
        for net_id in net_ids:
            net = im[net_id]
            print(net)


    return

class Network:
    def __init__(self, address) -> None:
        self.net = ipaddress.IPv4Network(address)
        self.subnets = set()
        self.addresses = set()

    def add_subnet(self, cidr):
        sn = ipaddress.IPv4Network((self.net.network_address, cidr))
        self.subnets.add(sn)

    def add_address(self, address):
        self.addresses.add(address)

    def assert_no_subnet_overlap(self):
        sns = [(s1, s2) for s1 in self.subnets for s2 in self.subnets if s1 != s2 and s1]