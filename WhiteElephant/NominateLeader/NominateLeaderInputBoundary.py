from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.NominateLeader.NominateLeaderOutputBoundary import NominateLeaderOutputBoundary
from WhiteElephant.infrastructure.Leader import Leader


@dataclass(frozen=True)
class NominateLeaderInputData:
    user: str
    leader: Leader
    game_id: str


class NominateLeaderInputBoundary(ABC):

    @abstractmethod
    async def execute(self, data: NominateLeaderInputData, presenter: NominateLeaderOutputBoundary) -> None: ...






