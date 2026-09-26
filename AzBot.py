import json

from WhiteElephant.CreateNewDraft.CreateNewDraftInputBoundary import CreateNewDraftInputBoundary
from WhiteElephant.CreateNewDraft.CreateNewDraftInteractor import CreateNewDraftInteractor
from WhiteElephant.DiscordCommands.CreateNewWhiteElephantDraft import CreateNewWhiteElephantDraft
from WhiteElephant.DiscordCommands.GetCurrentState import GetCurrentState
from WhiteElephant.DiscordCommands.NominateLeader import NominateLeader
from WhiteElephant.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputBoundary
from WhiteElephant.GetCurrentState.GetCurrentStateInteractor import GetCurrentStateInteractor
from WhiteElephant.NominateLeader.NominateLeaderInteractor import NominateLeaderInteractor
from WhiteElephant.entities.GameManager import GameManager
import lightbulb

import hikari

from WhiteElephant.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary


def get_guild() -> str:
    with open("guild.json") as f:
        file = f.read()
        guild = json.loads(file)["guild"]
    return guild

class AzBot:

    bot: hikari.GatewayBot
    client = lightbulb.Client
    guilds: list[hikari.OwnGuild]
    user_messages: dict[hikari.Snowflake, int]

    game_manager: GameManager


    def __init__(self, token: str, game_manager: GameManager) -> None:
        self.bot = hikari.GatewayBot(token)

        enabled_guild = int(get_guild())
        self.client = lightbulb.client_from_app(self.bot, default_enabled_guilds=[enabled_guild])

        self.bot.subscribe(hikari.StartingEvent, self.client.start)
        self.bot.subscribe(hikari.StoppingEvent, self.client.stop)


        self.game_manager = game_manager

        self.guilds = []
        self.user_messages = {}

        self.add_listeners()
        self.add_commands()

    def add_listeners(self) -> None:

        @self.bot.listen(hikari.StartedEvent)
        async def on_start(event: hikari.events.lifetime_events.StartedEvent):
            print("bot started")
            print(event)
            guilds = self.bot.rest.fetch_my_guilds()
            async for item in guilds:
                self.guilds.append(item)
            print(self.guilds)



        @self.bot.listen(hikari.VoiceStateUpdateEvent)
        async def voice_event_response(event: hikari.VoiceStateUpdateEvent):
            user_id = event.state.user_id
            user = await self.bot.rest.fetch_user(user_id)
            guild = await self.bot.rest.fetch_guild(event.guild_id)

            if event.state.channel_id is not None:
                channel = await self.bot.rest.fetch_channel(event.state.channel_id)
                print(f"\n{user} connected to: {channel} in: {guild}")
            elif event.old_state is not None:
                channel = await self.bot.rest.fetch_channel(event.old_state.channel_id)
                print(f"\n{user} left: {channel} in: {guild}, after talking for ")
            else:
                print(f"No current or previous state")



        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def message_response(event: hikari.events.message_events.GuildMessageCreateEvent):
            if not event.author.is_bot:


                print(f"\nAuthor: {event.author} | Content:{str(event.message.content)} \n"
                      f"Author_id: {event.author_id} | Guild: {event.get_guild()} \n"
                      f"Time_typing: ")



    def add_commands(self):

        interactor = NominateLeaderInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(NominateLeaderInputBoundary, interactor)
        self.client.register(NominateLeader)

        interactor = CreateNewDraftInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(CreateNewDraftInputBoundary, interactor)
        self.client.register(CreateNewWhiteElephantDraft)

        interactor = GetCurrentStateInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(GetCurrentStateInputBoundary, interactor)
        self.client.register(GetCurrentState)

        pass



