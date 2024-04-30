from __future__ import annotations

import datetime
import threading

import time
from abc import ABC

import lightbulb
from hikari import Event
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

from RedSquareGreenSquare import Game
from StopTypingEvent import StopTypingEvent
from TypingTracker import TypingTracker
from WriteToFileTextOutputBoundary import WriteToFileTextOutputBoundary

PrefixT = t.Union[
    t.Sequence[str],
    t.Callable[["BotApp", hikari.Message], t.Union[t.Sequence[str], t.Coroutine[t.Any, t.Any, t.Sequence[str]]]],
]


class AzBot(BotApp):

    guilds: list[hikari.OwnGuild]
    full_power: dict[hikari.Snowflake, bool]
    user_messages: dict[hikari.Snowflake, int]
    typing_tracker: TypingTracker

    def __init__(self, token: str) -> None:
        super().__init__(token=token)

        self.full_power = {}
        self.guilds = []
        self.user_messages = {}

        self.typing_tracker = TypingTracker(WriteToFileTextOutputBoundary("Typing_Time.txt"))

        self.add_listeners()
        self.add_commands()

    def add_listeners(self) -> None:

        @self.listen(hikari.StartedEvent)
        async def on_start(event: hikari.events.lifetime_events.StartedEvent):
            print("bot started")
            print(event)
            guilds = self.rest.fetch_my_guilds()
            async for item in guilds:
                self.guilds.append(item)
                self.full_power[item.id] = False
            print(self.guilds)
            print(self.full_power)

        """
        @bot.listen(hikari.GuildJoinEvent)
        async def join_guild(event: hikari.events.guild_events.GuildJoinEvent):
            print(type(event))
            guild = event.get_guild()

            new_category = await guild.create_category(name="Azcanta Land", position=3, reason="Azcanta's Home", )
            print(new_category.position)
            new_channel = await guild.create_text_channel(name="Azcanta's Lair", category=new_category)
        """

        @self.listen(hikari.VoiceEvent)
        async def voice_event_response(event: hikari.VoiceEvent):
            print(f"GildId: {event.guild_id} Shard: {event.shard} \n"
                  f"User Id {event.shard.get_user_id()}")

        @self.listen(hikari.GuildTypingEvent)
        async def typing_tracker(event: hikari.events.typing_events.GuildTypingEvent):
            # Triggers on the same typing every 8 seconds
            user = await self.rest.fetch_user(event.user_id)
            print(f"{user} started typing at: {event.timestamp}")
            self.typing_tracker.start_typing(event.user_id, event.timestamp)

            if self.full_power[event.guild_id]:

                if event.user_id == 208807710676746241:
                    return

                return_time = datetime.datetime.now() + datetime.timedelta(seconds=15)

                await self.rest.edit_member(guild=event.guild_id, user=user, communication_disabled_until=return_time)
                print(f" Timed out {user} for 15 seconds")


            # await self.dispatch(StopTypingEvent(event.app, event.user_id))

        @self.listen(hikari.GuildMessageCreateEvent)
        async def message_response(event: hikari.events.message_events.GuildMessageCreateEvent):
            if not event.author.is_bot:

                delta = self.typing_tracker.sent_message(event.author_id, event.message.timestamp)

                print(f"Author: {event.author} | Content:{str(event.content)} \n"
                      f"Author_id: {event.author_id} | Guild: {event.get_guild()} \n"
                      f"Time_typing: {delta}")

        """@self.listen(StopTypingEvent)
        async def stop_typing(event: StopTypingEvent):
            delta = self.typing_tracker.stop_typing(event.user)
            print(f"Time_typing: {delta}")"""

    def add_commands(self):
        @self.command()
        @lightbulb.command('fullpower', 'fullpower')
        @lightbulb.implements(lightbulb.SlashCommand)
        async def activate_full_power(ctx: lightbulb.context.slash.SlashContext):
            await ctx.respond("Full power activated, typing is no longer allowed")
            self.full_power[ctx.guild_id] = True
            print(self.full_power)

        @self.command()
        @lightbulb.command('lowpower', 'lowpower')
        @lightbulb.implements(lightbulb.SlashCommand)
        async def activate_full_power(ctx: lightbulb.context.slash.SlashContext):
            await ctx.respond("Full power de-activated, typing is now allowed")
            self.full_power[ctx.guild_id] = False
            print(self.full_power)
    """
    @staticmethod
    def _start_after_delay_on_new_thread(function: callable, seconds: int, args: any):
        asyncio.sleep(seconds)
        thread = threading.Thread(target=function, args=[args])
        thread.start()
    """





"""
make a typing time manager class
seoerate functionality

"""