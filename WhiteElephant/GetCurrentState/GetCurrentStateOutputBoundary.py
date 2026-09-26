from abc import ABC, abstractmethod
from dataclasses import dataclass

from WhiteElephant.infrastructure.Leader import Leader


@dataclass(frozen=True)
class GetCurrentStateOutputData:

    success: bool
    message: str
    users:list[str] | None = None

    nominated_leaders: list[Leader]| None = None
    user_nominated_leaders: dict[str, list[Leader]]| None = None

    started: bool| None = None

    turn_order: list[str]| None = None

    current_assignments: dict[str, list[Leader]]| None = None

    unselected_leaders: list[Leader]| None = None

    stolen_leaders: dict[str, int]| None = None
    stolen_picks: dict[str, list[int]]| None = None


class GetCurrentStateOutputBoundary(ABC):
    @abstractmethod
    async def present(self, output: GetCurrentStateOutputData ) -> None: ...