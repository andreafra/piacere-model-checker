import datetime
from z3 import sat, unsat
from .doml_mc import ModelChecker


def make_error(user_msg, debug_msg=None):
    result = {"message": user_msg, "timestamp": datetime.datetime.now()}
    if debug_msg is not None:
        result["debug_message"] = debug_msg
    return result


def post(body, requirement=None):
    doml_xmi = body
    try:
        dmc = ModelChecker(doml_xmi)
        result, msg = dmc.check_common_requirements(2)

        if result == sat:
            return {"result": "sat"}
        elif result == unsat:
            return {"result": "unsat",
                    "description": msg}
        else:
            return {"result": "dontknow",
                    "description": msg}

    except Exception as e:
        return make_error("The supplied DOMLX model is malformed or its DOML version is unsupported.", debug_msg=str(e)), 400
