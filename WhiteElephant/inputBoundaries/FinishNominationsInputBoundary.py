from abc import ABC, abstractmethod



class FinishNominationsInputBoundary(ABC):

    @abstractmethod
    async def finish_nominations(self, game_name: str) -> None:...
