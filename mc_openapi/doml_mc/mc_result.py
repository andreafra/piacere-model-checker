from enum import Enum
import logging
from typing import Literal
from z3 import CheckSatResult, sat, unsat, unknown


class MCResult(Enum):
    sat = 1
    unsat = 2
    dontknow = 3

    @staticmethod
    def from_z3result(z3res: CheckSatResult, flipped: bool = False) -> "MCResult":
        """Returns an Enum which is either sat, unsat or dontknow.
        If flipped is true, then the sat and unsat are swapped: it's useful when
        we are evaluating an expression in negative form.
        """
        if flipped:
            if z3res == sat:
                return MCResult.unsat
            elif z3res == unsat:
                return MCResult.sat
        else:
            if z3res == sat:
                return MCResult.sat
            elif z3res == unsat:
                return MCResult.unsat

        assert z3res == unknown
        return MCResult.dontknow


class MCResults:
    DONTKNOW_MSG = "Timed out: unable to check some requirements."
    SATISFIED_MSG = "All requirements are satisfied."

    def __init__(self, results: list[tuple[MCResult, Literal["BUILTIN", "USER"], str, str, str]]):
        """It receives a list of tuples (result, type, error message, id, desc, time)"""
        self.results = results

    def summarize(self) -> dict[str, any]:
        some_unsat = any(res == MCResult.unsat for res, _, _, _, _, _ in self.results)
        some_dontknow = any(res == MCResult.dontknow for res, _, _, _, _, _ in self.results)

        if some_unsat:
            builtin_err_msgs = [
                (id, msg, time) for res, type, msg, id, _, time in self.results if res == MCResult.unsat and type == "BUILTIN"]
            user_err_msgs = [
                (id, msg, time) for res, type, msg, id, _, time in self.results if res == MCResult.unsat and type == "USER"]

            # Print to text (instead of HTML)
            builtin_err_msg = "\n".join([f"[{id}][{time}s] {msg}" for id, msg, time in builtin_err_msgs])
            user_err_msg = "\n".join([f"[{id}][{time}s] {msg}" for id, msg, time  in user_err_msgs])

            err_msg = ""
            if builtin_err_msgs:
                err_msg += '[Built-in]\n' + builtin_err_msg
            if user_err_msgs:
                err_msg += '\n[User]\n' + user_err_msg
            if some_dontknow:
                err_msg += '\n' + MCResults.DONTKNOW_MSG
            
            all_reqs = [
                {
                    "id": id,
                    "type": type,
                    "message": msg,
                    "result": res.name,
                    "description": desc,
                    "time": time
                }
                for res, type, msg, id, desc, time in self.results
            ]

            return {
                'result': MCResult.unsat,
                'builtin': builtin_err_msgs,
                'user': user_err_msgs,
                'dontknow': some_dontknow,
                'description': err_msg,
                'all_reqs': all_reqs
            }
        elif some_dontknow:
            return {'result': MCResult.dontknow, 'description': MCResults.DONTKNOW_MSG }
        else:
            return {'result': MCResult.sat, 'description': MCResults.SATISFIED_MSG }

    def add_results(self, results: "MCResults"):
        self.results.extend(results.results)
