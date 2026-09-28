"""
Interface for saving and loading game state.

"""
from abc import ABC, abstractmethod


class GameStateStore(ABC):
    @abstractmethod
    def save(self, game_id: str, state: dict) -> None:
        """Record the latest state of a game."""

    @abstractmethod
    def delete(self, game_id: str) -> None:
        """Record that a game no longer exists."""

    @abstractmethod
    def load_all(self) -> dict[str, dict]:
        """Return {game_id: latest saved state} for every game that still exists."""


class NullGameStateStore(GameStateStore):
    """
    Empty store for cases where state storing is not desired
    """

    def save(self, game_id: str, state: dict) -> None:
        pass

    def delete(self, game_id: str) -> None:
        pass

    def load_all(self) -> dict[str, dict]:
        return {}