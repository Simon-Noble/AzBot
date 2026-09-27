from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.NominateLeader.NominateLeaderOutputBoundary import NominateLeaderOutputBoundary


@dataclass(frozen=True)
class NominateLeaderInputData:
    user: str
    leader_id: str
    game_id: str


class NominateLeaderInputBoundary(ABC):

    @abstractmethod
    async def execute(self, data: NominateLeaderInputData, presenter: NominateLeaderOutputBoundary) -> None: ...






