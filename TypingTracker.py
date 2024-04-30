from datetime import datetime, timedelta

from hikari import Snowflake

from TextOutputBoundary import TextOutputBoundary


class TypingTracker:
    """
    Manages tracking typing times for various users


    """

    currently_typing: dict[Snowflake: datetime]  # who is currently typing, when they started, and most
    #                                                          recent typing activity
    typing_totals: dict[Snowflake: timedelta]  # total typing time in the tracking period
    output_boundary: TextOutputBoundary

    def __init__(self, output_boundary: TextOutputBoundary):
        self.currently_typing = {}
        self.typing_totals = {}
        self.output_boundary = output_boundary

    def _add_typing_time(self, user: Snowflake, delta: timedelta):
        if user in self.typing_totals:
            self.typing_totals[user] += delta
        else:
            self.typing_totals[user] = delta

    def start_typing(self, user: Snowflake, typing_time: datetime):
        """
        Record that a user has started typing
        If that user is already typing reset their typing and add the difference to their time


        """
        if user in self.currently_typing:
            delta: timedelta = self.currently_typing[user] - typing_time

            if delta > timedelta(seconds=10):
                self._add_typing_time(user, timedelta(seconds=4))
            else:
                self._add_typing_time(user, delta)

        self.currently_typing[user] = typing_time

    def sent_message(self, user: Snowflake, sent_time: datetime):
        """
        If the user was typing in the previous 8 seconds, take the difference ad att it to their typing total

        :param user:
        :param sent_time:
        :return:
        """

        if user not in self.currently_typing:
            return

        delta: timedelta = sent_time - self.currently_typing[user]

        if delta > timedelta(seconds=10):
            self._add_typing_time(user, timedelta(seconds=4))
        else:
            self._add_typing_time(user, delta)

        self.currently_typing.pop(user)

        self.output_boundary.write(str(self.typing_totals))
        return delta

