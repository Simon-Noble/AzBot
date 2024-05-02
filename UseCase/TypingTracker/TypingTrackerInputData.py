from dataclasses import dataclass
from datetime import datetime


@dataclass
class TypingTrackerInputData:
    user: str
    time: datetime
