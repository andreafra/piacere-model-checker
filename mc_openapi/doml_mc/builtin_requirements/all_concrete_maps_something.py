from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name
from . import CELEMS_V2_0, CELEMS_V3_1

# All elements in the active concretization are mapped to some abstract infrastructure element.

def all_concrete_map_something(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    def checkOneClass(ielem, provider, celem, providerAssoc, celemAssoc):
        return And(
            smtenc.association_rel(
                provider, smtenc.associations[providerAssoc], celem),
            Not(
                Exists(
                    [ielem],
                    smtenc.association_rel(
                        celem, smtenc.associations[celemAssoc], ielem)
                )
            )
        )

    ielem, concr, provider, celem = Consts(
       "ielem concr provider celem", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            concr) == smtenc.classes["concrete_ConcreteInfrastructure"],
        smtenc.association_rel(
            concr, smtenc.associations["concrete_ConcreteInfrastructure::providers"], provider),
        Or(
            *(
                checkOneClass(
                    ielem, provider, celem,
                    providerAssoc, celemAssoc
                )
                for _, providerAssoc, celemAssoc in CELEMS_V2_0
            )
        )
    )

def all_concrete_map_something_v3_1(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    def checkOneClass(ielem, provider, celem, providerAssoc, celemAssoc):
        return And(
            smtenc.association_rel(
                provider, smtenc.associations[providerAssoc], celem),
            Not(
                Exists(
                    [ielem],
                    smtenc.association_rel(
                        celem, smtenc.associations[celemAssoc], ielem)
                )
            )
        )

    ielem, concr, provider, celem = Consts(
       "ielem concr provider celem", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            concr) == smtenc.classes["concrete_ConcreteInfrastructure"],
        smtenc.association_rel(
            concr, smtenc.associations["concrete_ConcreteInfrastructure::providers"], provider),
        Or(
            *(
                checkOneClass(
                    ielem, provider, celem,
                    providerAssoc, celemAssoc
                )
                for _, providerAssoc, celemAssoc in CELEMS_V3_1
            )
        )
    )


def ed_all_concrete_map_something(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        celem = Const("celem", smtsorts.element_sort)
        celem_name = get_user_friendly_name(
            intermediate_model, solver.model(), celem)
        if celem_name:
            return f"Concrete infrastructure element '{celem_name}' is not mapped to any abstract infrastructure element."
    except:
        return "A concrete infrastructure element is not mapped to any abstract infrastructure element."

MSG = "All elements in the active concretization are mapped to some abstract infrastructure element."

ALL_CONCRETE_MAP_SOMETHING = (
    all_concrete_map_something,
    "all_concrete_map_something",
    MSG,
    ed_all_concrete_map_something
)

ALL_CONCRETE_MAP_SOMETHING_V3_1 = (
    all_concrete_map_something_v3_1,
    "all_concrete_map_something",
    MSG,
    ed_all_concrete_map_something
)