
class WhiteElephantOutput:
    def __init__(self):
        pass

    def prepareFail(self, message:str) -> None:
        raise NotImplementedError()

    def prepareSuccess(self, message: str):
        raise NotImplementedError()