import datetime
import json

import lightbulb
from lightbulb import BotApp

import hikari

from TalkingTracker import TalkingTracker
from TypingTracker import TypingTracker
from WriteToFileTextOutputBoundary import WriteToFileTextOutputBoundary


class AzBot(BotApp):

    guilds: list[hikari.OwnGuild]
    full_power: dict[hikari.Snowflake, bool]
    user_messages: dict[hikari.Snowflake, int]
    typing_tracker: TypingTracker
    talking_tracker: TalkingTracker

    def __init__(self, token: str) -> None:
        super().__init__(token=token)

        self.full_power = {}
        self.guilds = []
        self.user_messages = {}

        with open("Typing_Time.txt") as f:
            typing_file = f.read()
            starting_typing = json.loads(typing_file)
        typing_output_boundary = WriteToFileTextOutputBoundary("Typing_Time.txt")
        self.typing_tracker = TypingTracker(typing_output_boundary, starting_typing)

        with open("Talking_Time.txt") as f:
            talking_file = f.read()
            starting_talking = json.loads(talking_file)
        talking_output_boundary = WriteToFileTextOutputBoundary("Talking_Time.txt")
        self.talking_tracker = TalkingTracker(talking_output_boundary, starting_talking)

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

            new_category = await guild.create_category(name="Azcanta Land", position=3, reason="Azcanta's Home")
            print(new_category.position)
            new_channel = await guild.create_text_channel(name="Azcanta's Lair", category=new_category)
        """

        @self.listen(hikari.VoiceStateUpdateEvent)
        async def voice_event_response(event: hikari.VoiceStateUpdateEvent):
            user_id = event.state.user_id
            user = await self.rest.fetch_user(user_id)
            guild = await self.rest.fetch_guild(event.guild_id)
            talking_time = datetime.datetime.now()

            if event.state.channel_id is not None:
                channel = await self.rest.fetch_channel(event.state.channel_id)
                self.talking_tracker.join_call(user.username, talking_time)
                print(f"\n{user} connected to: {channel} in: {guild}")
            elif event.old_state is not None:
                channel = await self.rest.fetch_channel(event.old_state.channel_id)
                delta = self.talking_tracker.leave_call(user.username, talking_time)
                print(f"\n{user} left: {channel} in: {guild}, after talking for {delta}")
            else:
                print(f"No current or previous state")

        @self.listen(hikari.GuildTypingEvent)
        async def typing_tracker(event: hikari.events.typing_events.GuildTypingEvent):
            # Triggers on the same typing every 8 seconds
            user = await self.rest.fetch_user(event.user_id)
            print(f"{user} started typing at: {event.timestamp}")
            self.typing_tracker.start_typing(user.username, event.timestamp)

            if self.full_power[event.guild_id]:

                if event.user_id == 208807710676746241:
                    return

                return_time = event.timestamp + datetime.timedelta(seconds=15)

                await self.rest.edit_member(guild=event.guild_id, user=user, communication_disabled_until=return_time)
                print(f" Timed out {user} for 15 seconds")
            # await self.dispatch(StopTypingEvent(event.app, event.user_id))

        @self.listen(hikari.GuildMessageCreateEvent)
        async def message_response(event: hikari.events.message_events.GuildMessageCreateEvent):
            if not event.author.is_bot:

                delta = self.typing_tracker.sent_message(event.author.username, event.message.timestamp)

                print(f"\nAuthor: {event.author} | Content:{str(event.message.content)} \n"
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
