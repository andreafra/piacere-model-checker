from typing import Optional
from joblib import parallel_backend, Parallel, delayed
from multiprocessing import TimeoutError

from .intermediate_model.metamodel import (
    DOMLVersion,
    MetaModels,
    InverseAssociations
)
from .xmi_parser.doml_model import parse_doml_model
from .mc_result import MCResult, MCResults
from .imc import RequirementStore, IntermediateModelChecker
from .common_reqs import CommonRequirements
from .consistency_reqs import (
    get_attribute_type_reqs,
    get_attribute_multiplicity_reqs,
    get_association_type_reqs,
    get_association_multiplicity_reqs,
    get_inverse_association_reqs
)


class ModelChecker:
    def __init__(self, xmi_model: bytes, doml_version: Optional[DOMLVersion] = None):
        self.intermediate_model, doml_version = parse_doml_model(xmi_model, doml_version)
        self.metamodel = MetaModels[doml_version]
        self.inv_assoc = InverseAssociations[doml_version]

    def check_common_requirements(self, threads: int = 1, consistency_checks: bool = False, timeout: Optional[int] = None) -> MCResults:
        assert self.metamodel and self.inv_assoc
        req_store = CommonRequirements
        if consistency_checks:
            req_store = req_store \
                + get_attribute_type_reqs(self.metamodel) \
                + get_attribute_multiplicity_reqs(self.metamodel) \
                + get_association_type_reqs(self.metamodel) \
                + get_association_multiplicity_reqs(self.metamodel) \
                + get_inverse_association_reqs(self.inv_assoc)

        def worker(rfrom: int, rto: int):
            imc = IntermediateModelChecker(self.metamodel, self.inv_assoc, self.intermediate_model)
            rs = RequirementStore(req_store.get_all_requirements()[rfrom:rto])
            return imc.check_requirements(rs)

        if threads <= 1:
            imc = IntermediateModelChecker(self.metamodel, self.inv_assoc, self.intermediate_model)
            reqs = imc.check_requirements(req_store, timeout=(0 if timeout is None else timeout))
            return reqs
        else:
            def split_reqs(n_reqs: int, n_split: int):
                slice_size = n_reqs // n_split
                rto = 0
                while rto < n_reqs:
                    rfrom = rto
                    rto = min(rfrom + slice_size, n_reqs)
                    yield rfrom, rto

            try:
                with parallel_backend('loky', n_jobs=threads):
                    results = Parallel(timeout=timeout)(delayed(worker)(rfrom, rto) for rfrom, rto in split_reqs(len(req_store), threads))
                ret = MCResults([])
                for res in results:
                    ret.add_results(res)
                return ret
            except TimeoutError:
                return MCResults([(MCResult.dontknow, "")])
