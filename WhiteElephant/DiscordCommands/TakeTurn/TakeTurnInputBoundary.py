from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnOutputBoundary import TakeTurnOutputBoundary


@dataclass(frozen=True)
class TakeTurnInputData:
    game_id: str
    steal: bool
    user: str

    leader_to_steal: str | None = None


class TakeTurnInputBoundary(ABC):
    @abstractmethod
    async def execute(self, data: TakeTurnInputData, presenter: TakeTurnOutputBoundary) -> None:...