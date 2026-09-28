from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData


@dataclass(frozen=True)
class TakeTurnOutputData(GenericStateOutputData):
    pass


class TakeTurnOutputBoundary(ABC):
    @abstractmethod
    async def present(self, output: TakeTurnOutputData ) -> None: ...