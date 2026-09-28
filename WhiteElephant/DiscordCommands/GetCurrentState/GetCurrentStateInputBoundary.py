from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateOutputBoundary import GetCurrentStateOutputBoundary


@dataclass(frozen=True)
class GetCurrentStateInputData:
    game_id: str


class GetCurrentStateInputBoundary(ABC):
    @abstractmethod
    async def execute(self, data: GetCurrentStateInputData, presenter: GetCurrentStateOutputBoundary) -> None:...