from dataclasses import dataclass
from abc import ABC, abstractmethod

from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftOutputBoundary import CreateNewDraftOutputBoundary


@dataclass
class CreateNewDraftInputData:
    users: list[str]
    game_id: str

class CreateNewDraftInputBoundary(ABC):
    @abstractmethod
    async def execute(self, data: CreateNewDraftInputData, presenter: CreateNewDraftOutputBoundary) -> None:...
