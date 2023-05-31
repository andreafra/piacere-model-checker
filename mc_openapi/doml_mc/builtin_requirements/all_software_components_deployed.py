from z3 import And, Const, Consts, Exists, ExprRef, Not, Or, Solver, Implies
from mc_openapi.doml_mc.imc import Requirement, SMTEncoding, SMTSorts
from mc_openapi.doml_mc.intermediate_model import DOMLVersion, IntermediateModel
from mc_openapi.doml_mc.error_desc_helper import get_user_friendly_name

# All software components have been deployed to some node.

def all_software_components_deployed(smtenc: SMTEncoding, smtsorts: SMTSorts) -> ExprRef:
    sc, deployment, ielem = Consts("sc deployment ielem", smtsorts.element_sort)
    return And(
        smtenc.element_class_fun(
            sc) == smtenc.classes["application_SoftwareComponent"],
        Not(
            Exists(
                [deployment, ielem],
                And(
                    smtenc.association_rel(
                        deployment, smtenc.associations["commons_Deployment::component"], sc),
                    smtenc.association_rel(
                        deployment, smtenc.associations["commons_Deployment::node"], ielem),
                )
            )
        )
    )

def ed_all_software_components_deployed(solver: Solver, smtsorts: SMTSorts, intermediate_model: IntermediateModel) -> str:
    try:
        sc = Const("sc", smtsorts.element_sort)
        sc_name = get_user_friendly_name(
            intermediate_model, solver.model(), sc)
        if sc_name:
            return f"Software component '{sc_name}' is not deployed to any abstract infrastructure node."
    except:
        return "A software component is not deployed to any abstract infrastructure node."

MSG = "All software components have been deployed to some node."

ALL_SOFTWARE_COMPONENTS_DEPLOYED = (
    all_software_components_deployed,
    "all_software_components_deployed",
    MSG,
    ed_all_software_components_deployed
)