from abc import ABC, abstractmethod

class DraftRandomLeaderInputBoundary(ABC):

    @abstractmethod
    async def draft_random_leader(self, user, game_name: str) -> None: ...


