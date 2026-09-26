from dataclasses import dataclass

@dataclass(frozen=True)
class Leader:
    id: str
    name: str
    civ: str
    leader_emoji: str
    civ_emoji: str