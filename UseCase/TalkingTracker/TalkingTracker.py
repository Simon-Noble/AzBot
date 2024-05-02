from datetime import datetime, timedelta

from TextOutputBoundary import TextOutputBoundary
from UseCase.TalkingTracker.TalkingTrackerInputBoundary import TalkingTrackerInputBoundary
from UseCase.TalkingTracker.TalkingTrackerInputData import TalkingTrackerInputData


class TalkingTracker(TalkingTrackerInputBoundary):

    currently_in_call: dict[str: datetime]
    total_call_times: dict[str: int]
    output_boundary: TextOutputBoundary

    def __init__(self, output_boundary: TextOutputBoundary,
                 starting_state: dict[str: timedelta] = None):
        self.currently_in_call = {}
        if starting_state is not None:
            self.total_call_times = starting_state
        else:
            self.total_call_times = {}
        self.output_boundary = output_boundary

    def _add_talking_time(self, user: str, delta: timedelta):
        if user in self.total_call_times:
            self.total_call_times[user] += int(delta.seconds)
        else:
            self.total_call_times[user] = int(delta.seconds)

    def join_call(self, input_data: TalkingTrackerInputData):
        if input_data.user in self.currently_in_call:
            return

        self.currently_in_call[input_data.user] = input_data.time

    def leave_call(self, input_data: TalkingTrackerInputData):
        if input_data.user not in self.currently_in_call:
            return timedelta(0)

        start_time = self.currently_in_call.pop(input_data.user)
        delta = input_data.time - start_time
        self._add_talking_time(input_data.user, delta)
        self.output_boundary.write(self.total_call_times)

        return delta
