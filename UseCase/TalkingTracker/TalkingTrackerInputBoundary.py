from datetime import datetime
from UseCase.TalkingTracker.TalkingTrackerInputData import TalkingTrackerInputData


class TalkingTrackerInputBoundary:

    def join_call(self, input_data: TalkingTrackerInputData):
        raise NotImplementedError

    def leave_call(self, input_data: TalkingTrackerInputData):
        raise NotImplementedError
