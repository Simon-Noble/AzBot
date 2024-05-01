from datetime import datetime, timedelta

from TextOutputBoundary import TextOutputBoundary


class TalkingTracker:

    currently_in_call: dict[str: datetime]
    total_call_times: dict[str: timedelta]
    output_boundary: TextOutputBoundary

    def __init__(self, output_boundary: TextOutputBoundary):
        self.currently_in_call = {}
        self.total_call_times = {}
        self.output_boundary = output_boundary

    def _add_talking_time(self, user: str, delta: timedelta):
        if user in self.total_call_times:
            self.total_call_times[user] += delta
        else:
            self.total_call_times[user] = delta

    def join_call(self, user_name: str, time: datetime):
        if user_name in self.currently_in_call:
            return

        self.currently_in_call[user_name] = time

    def leave_call(self, user_name: str, time: datetime) -> timedelta:
        if user_name not in self.currently_in_call:
            return timedelta(0)

        start_time = self.currently_in_call.pop(user_name)

        delta = time - start_time

        self._add_talking_time(user_name, delta)

        self.output_boundary.write(str(self.total_call_times))

        return delta