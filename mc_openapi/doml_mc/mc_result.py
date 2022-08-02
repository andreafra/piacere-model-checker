from enum import Enum
from z3 import CheckSatResult, sat, unsat, unknown


class MCResult(Enum):
    sat = 1
    unsat = 2
    dontknow = 3

    @staticmethod
    def from_z3result(z3res: CheckSatResult, flipped: bool = False) -> "MCResult":
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
    dontknow_msg = "Timed out: unable to check some requirements."

    def __init__(self, results: list[tuple[MCResult, str]]):
        self.results = results

    def summarize(self) -> tuple[MCResult, str]:
        some_unsat = any(res == MCResult.unsat for res, _ in self.results)
        some_dontknow = any(res == MCResult.dontknow for res, _ in self.results)

        if some_unsat:
            err_msg = " ".join(msg for res, msg in self.results if res == MCResult.unsat)
            if some_dontknow:
                err_msg = err_msg + MCResults.dontknow_msg
            return MCResult.unsat, err_msg
        elif some_dontknow:
            return MCResult.dontknow, MCResults.dontknow_msg
        else:
            return MCResult.sat, "All requirements satisfied."

    def add_result(self, result: tuple[MCResult, str]):
        self.results.append(result)

    def add_results(self, results: "MCResults"):
        self.results.extend(results.results)
