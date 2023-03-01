from typing import Optional, Tuple
import copy
import importlib.resources as ilres
from lxml import etree
from ipaddress import ip_address, ip_network

from mc_openapi import assets
from mc_openapi.bytes_uri import BytesURI
from pyecore.ecore import EObject
from pyecore.resources import ResourceSet

from ..intermediate_model.doml_element import Attributes, IntermediateModel, reciprocate_inverse_associations
from ..intermediate_model.metamodel import DOMLVersion, MetaModels, InverseAssociations
from .ecore import ELayerParser, SpecialParser


doml_rsets = {}
def init_doml_rsets():  # noqa: E302
    global doml_rsets
    for ver in DOMLVersion:
        rset = ResourceSet()
        resource = rset.get_resource(BytesURI(
            "doml", bytes=ilres.read_binary(assets, f"doml_{ver.value}.ecore")
        ))
        doml_metamodel = resource.contents[0]

        rset.metamodel_registry[doml_metamodel.nsURI] = doml_metamodel
        for subp in doml_metamodel.eSubpackages:
            rset.metamodel_registry[subp.nsURI] = subp

        doml_rsets[ver] = rset


def get_rset(doml_version: DOMLVersion) -> ResourceSet:
    return copy.copy(doml_rsets[doml_version])


def parse_xmi_model(raw_model: bytes, doml_version: DOMLVersion) -> EObject:
    rset = get_rset(doml_version)
    doml_uri = BytesURI("user_doml", bytes=raw_model)
    resource = rset.create_resource(doml_uri)
    resource.load()
    return resource.contents[0]


def infer_domlx_version(raw_model: bytes) -> DOMLVersion:
    root = etree.fromstring(raw_model)
    if root.tag == "{http://www.piacere-project.eu/doml/commons}DOMLModel":
        if "version" in root.attrib:
            v_str = root.attrib["version"]
            try:
                return DOMLVersion(v_str)
            except ValueError:
                if v_str == "v2":
                    return DOMLVersion.V2_0
                else:
                    raise RuntimeError(f"Supplied with DOMLX model of unsupported version {v_str}")
        else:
            return DOMLVersion.V1_0
    else:
        raise RuntimeError("Supplied with malformed DOMLX model.")


def parse_doml_model(raw_model: bytes, doml_version: Optional[DOMLVersion]) -> Tuple[IntermediateModel, DOMLVersion]:
    def parse_network_address_range(arange: str) -> Attributes:
        ipnet = ip_network(arange)
        return {"address_lb": [int(ipnet[0])], "address_ub": [int(ipnet[-1])]}

    def parse_iface_address(addrport: str) -> Attributes:
        addr, _, port = addrport.rpartition(":")
        if addr == "":
            addr = port
        return {"endPoint": [int(ip_address(addr))]}

    if doml_version is None:
        doml_version = infer_domlx_version(raw_model)

    model = parse_xmi_model(raw_model, doml_version)

    mm = MetaModels[doml_version]
    sp = SpecialParser(mm, {
        ("infrastructure_Network", "addressRange"): parse_network_address_range,
        ("infrastructure_NetworkInterface", "endPoint"): parse_iface_address,
        ("infrastructure_ComputingNode", "memory_mb"): lambda mem: {"memory_mb":  [int(mem)], "memory_kb": [int(mem * 1024)]},
        ("commons_FProperty", "value"): lambda fval: {"value": [str(fval)]},
    })
    elp = ELayerParser(mm, sp)
    if model.application:
        elp.parse_elayer(model.application)
    if model.infrastructure:
        elp.parse_elayer(model.infrastructure)
    else:
        raise RuntimeError("Abstract infrastructure layer is missing.")
    if model.activeConfiguration:
        elp.parse_elayer(model.activeConfiguration)
    if model.activeInfrastructure:
        im = elp.parse_elayer(model.activeInfrastructure)
    else:
        raise RuntimeError("No active concrete infrastructure layer has been specified.")

    reciprocate_inverse_associations(im, InverseAssociations[doml_version])

    return im, doml_version
