from dataclasses import dataclass
from datetime import datetime


@dataclass
class TalkingTrackerInputData:
    user: str
    time: datetime