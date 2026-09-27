from abc import abstractmethod, ABC
from dataclasses import dataclass

from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData


@dataclass(frozen=True)
class FinishNominationsOutputData(GenericStateOutputData):
    pass

class FinishNominationsOutputBoundary(ABC):
    @abstractmethod
    async def present(self, data: FinishNominationsOutputData) -> None:
        pass