from mc_openapi.doml_mc.intermediate_model.metamodel import DOMLVersion


class BadDOMLException(Exception):
    def __init__(self, message: str = None, *args: object) -> None:
        super().__init__(*args)
        self.message = message or "The submitted DOML contains some kind of error."

class UnsupportedDOMLVersionException(Exception):
    def __init__(self, message: str = None, *args: object) -> None:
        super().__init__(*args)
        self.message = message or "The DOML version is not supported."

class MissingInfrastructureLayerException(Exception):
    def __init__(self, message: str = None, *args: object) -> None:
        super().__init__(*args)
        self.message = message or "Abstract infrastructure layer is missing from DOML."

class NoActiveConcreteLayerException(Exception):
    def __init__(self, message: str = None, *args: object) -> None:
        super().__init__(*args)
        self.message = message or "No active concrete infrastructure layer has been specified in DOML."

