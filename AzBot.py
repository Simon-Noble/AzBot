from __future__ import annotations

from abc import ABC

from lightbulb import BotApp
import asyncio
import collections.abc
import functools
import importlib
import inspect
import logging
import os
import pathlib
import re
import sys
import typing as t
from importlib import util

import hikari
from hikari.internal import ux
from multidict import CIMultiDict

from lightbulb import checks
from lightbulb import commands
from lightbulb import context as context_
from lightbulb import decorators
from lightbulb import errors
from lightbulb import events
from lightbulb import help_command as help_command_
from lightbulb import internal
from lightbulb import plugins as plugins_
from lightbulb.utils import data_store
from lightbulb.utils import parser

from RedSquareGreenSquare import Game

PrefixT = t.Union[
    t.Sequence[str],
    t.Callable[["BotApp", hikari.Message], t.Union[t.Sequence[str], t.Coroutine[t.Any, t.Any, t.Sequence[str]]]],
]


class AzBot(BotApp):

    guilds: list[hikari.OwnGuild]
    full_power: dict[hikari.Snowflake, bool]
    tent_games: dict[hikari.snowflakes, Game]

    def __init__(self,
                 token: str,
                 prefix: t.Optional[PrefixT] = None,
                 ignore_bots: bool = True,
                 owner_ids: t.Sequence[int] = (),
                 default_enabled_guilds: t.Union[int, t.Sequence[int]] = (),
                 help_class: t.Optional[t.Type[help_command_.BaseHelpCommand]] = help_command_.DefaultHelpCommand,
                 help_slash_command: bool = False,
                 delete_unbound_commands: bool = True,
                 case_insensitive_prefix_commands: bool = False,
                 **kwargs: t.Any
                 ) -> None:
        super().__init__(token=token, prefix=prefix, ignore_bots=ignore_bots, owner_ids=owner_ids,
                         default_enabled_guilds=default_enabled_guilds, help_class=help_class,
                         help_slash_command=help_slash_command, delete_unbound_commands=delete_unbound_commands,
                         case_insensitive_prefix_commands=case_insensitive_prefix_commands
                         )
        self.guilds = []
        self.full_power = {}
        self.tent_games = {}

    def get_game(self, user: hikari.snowflakes) -> Game:
        if user in self.tent_games:
            return self.tent_games[user]
        else:
            self.tent_games[user] = Game()
            return self.tent_games[user]