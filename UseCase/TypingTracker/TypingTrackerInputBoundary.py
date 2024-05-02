from datetime import datetime
from UseCase.TypingTracker.TypingTrackerInputData import TypingTrackerInputData


class TypingTrackerInputBoundary:

    def start_typing(self, input_data: TypingTrackerInputData):
        raise NotImplementedError

    def sent_message(self, input_data: TypingTrackerInputData):
        raise NotImplementedError
