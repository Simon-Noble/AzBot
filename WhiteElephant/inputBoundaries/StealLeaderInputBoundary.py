from abc import ABC, abstractmethod

class StealLeaderInputBoundary(ABC):
    @abstractmethod
    async def steal(self, user: str, game_name: str, player_to_steal_from: str) -> None:...

