from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CreateNewDraftOutputData:
    success: bool
    message: str



class CreateNewDraftOutputBoundary(ABC):

    @abstractmethod
    async def present(self, output: CreateNewDraftOutputData) -> None:
        pass