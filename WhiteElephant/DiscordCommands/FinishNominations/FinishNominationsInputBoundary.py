from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsOutputBoundary import FinishNominationsOutputBoundary


@dataclass(frozen=True)
class FinishNominationsInputData:
    game_id:str


class FinishNominationsInputBoundary(ABC):

    @abstractmethod
    async def execute(self, data: FinishNominationsInputData, presenter: FinishNominationsOutputBoundary) -> None:...
