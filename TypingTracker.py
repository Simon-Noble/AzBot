from datetime import datetime, timedelta

from hikari import Snowflake


class TypingTracker:
    """
    Manages tracking typing times for various users


    """

    currently_typing: dict[Snowflake: datetime]  # who is currently typing, when they started, and most
    #                                                          recent typing activity
    typing_totals: dict[Snowflake: timedelta]  # total typing time in the tracking period

    def __init__(self):
        self.currently_typing = {}
        self.typing_totals = {}

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

        self._add_typing_time(user, delta)

        self.currently_typing.pop(user)

        return delta

    def stop_typing(self, user: Snowflake):
        """
        It has been long enough since the last time event, add 4 seconds to the delta and
        remove them from current typers
        :return:
        """
        if user not in self.currently_typing:
            return

        self.currently_typing.pop(user)

        self._add_typing_time(user, timedelta(seconds=4))
