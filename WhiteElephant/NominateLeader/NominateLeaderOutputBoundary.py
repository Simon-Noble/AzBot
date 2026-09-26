from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.infrastructure.Leader import Leader


@dataclass
class NominateLeaderOutputData:
    success: bool
    message: str
    leader: Leader | None = None


class NominateLeaderOutputBoundary(ABC):
    @abstractmethod
    async def present(self, output: NominateLeaderOutputData) -> None: ...