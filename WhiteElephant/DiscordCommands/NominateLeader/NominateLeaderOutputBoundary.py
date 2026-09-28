from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class NominateLeaderOutputData:
    success: bool
    message: str
    leader: str | None = None


class NominateLeaderOutputBoundary(ABC):
    @abstractmethod
    async def present(self, output: NominateLeaderOutputData) -> None: ...