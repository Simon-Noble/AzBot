from dataclasses import dataclass




@dataclass(frozen=True)
class GenericStateOutputData:
    success: bool
    message: str
    users: list[str] | None = None

    nominated_leaders: list[str] | None = None
    user_nominated_leaders: dict[str, list[str]] | None = None

    started: bool | None = None

    turn_order: list[str] | None = None

    current_assignments: dict[str, list[str]] | None = None

    unselected_leaders: list[str] | None = None

    stolen_leaders: dict[str, int] | None = None
    stolen_picks: dict[str, int] | None = None
    current_chain:list[str] | None = None
