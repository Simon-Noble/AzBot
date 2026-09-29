from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData


@dataclass(frozen=True)
class GetCurrentStateOutputData(GenericStateOutputData):
    prompt_current_player: bool = False


class GetCurrentStateOutputBoundary(ABC):
    @abstractmethod
    async def present(self, output: GetCurrentStateOutputData ) -> None: ...