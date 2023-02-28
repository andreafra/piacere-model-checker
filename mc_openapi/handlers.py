import datetime
from mc_openapi.doml_mc.domlr_parser.parser import DOMLRTransformer, Parser
from mc_openapi.doml_mc.imc import RequirementStore

from mc_openapi.doml_mc.intermediate_model.metamodel import DOMLVersion
from mc_openapi.doml_mc.xmi_parser.doml_model import get_pyecore_model
from .doml_mc import ModelChecker, MCResult


def make_error(user_msg, debug_msg=None):
    result = {"message": user_msg, "timestamp": datetime.datetime.now()}
    if debug_msg is not None:
        result["debug_message"] = debug_msg
        print(f"ERROR [{datetime.datetime.now()}]: {debug_msg}")
    return result


def post(body):
    doml_xmi = body
    try:

        dmc = ModelChecker(doml_xmi)

        user_req_store = None
        user_req_str_consts = []

        # Add support for Requirements in DOML
        if dmc.doml_version == DOMLVersion.V2_2:
                domlr_parser = Parser(DOMLRTransformer)
                model = get_pyecore_model(doml_xmi, DOMLVersion.V2_2)
                func_reqs = model.functionalRequirements.items

                user_req_store = RequirementStore()

                for req in func_reqs:
                    req_name: str = req.name
                    req_text: str = req.description
                    req_text = req_text.replace("```", "")
                    doml_req_store, doml_req_str_consts = domlr_parser.parse(req_text)
                    user_req_store += doml_req_store
                    user_req_str_consts += doml_req_str_consts


        results = dmc.check_requirements(threads=2, user_requirements=user_req_store, user_str_values=user_req_str_consts, consistency_checks=False, timeout=50)
        res, msg = results.summarize()

        if res == MCResult.sat:
            return {"result": "sat"}
        else:
            return {"result": res.name,
                    "description": msg}

    # TODO: Make noteworthy exceptions to at least tell the user what is wrong
    except Exception as e:
        return make_error("The supplied DOMLX model is malformed or its DOML version is unsupported.", debug_msg=str(e)), 400
