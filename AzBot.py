import json


import lightbulb

import hikari

from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftInputBoundary import CreateNewDraftInputBoundary
from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftInteractor import CreateNewDraftInteractor
from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewWhiteElephantDraftCommand import CreateNewWhiteElephantDraftCommand
from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsCommand import FinishNominationsCommand
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateCommand import GetCurrentStateCommand
from WhiteElephant.DiscordCommands.NominateLeader.NominateLeaderCommand import NominateLeaderCommand
from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsInputBoundary import FinishNominationsInputBoundary
from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsInteractor import FinishNominationsInteractor
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputBoundary
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateInteractor import GetCurrentStateInteractor
from WhiteElephant.DiscordCommands.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary
from WhiteElephant.DiscordCommands.NominateLeader.NominateLeaderInteractor import NominateLeaderInteractor
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInteractor import TakeTurnInteractor
from WhiteElephant.entities.GameManager import GameManager
from WhiteElephant.infrastructure.LeaderManager import LeaderManager


def get_guilds() -> list[str]:
    with open("guild.json") as f:
        file = f.read()
        guild = json.loads(file)["guilds"]
    return guild

class AzBot:

    bot: hikari.GatewayBot
    client = lightbulb.Client
    guilds: list[hikari.OwnGuild]
    user_messages: dict[hikari.Snowflake, int]

    game_manager: GameManager
    leader_manager: LeaderManager


    def __init__(self, token: str, game_manager: GameManager) -> None:
        self.bot = hikari.GatewayBot(token)

        enabled_guild = [int(guild) for guild in get_guilds()]
        self.client = lightbulb.client_from_app(self.bot, default_enabled_guilds=enabled_guild)

        self.bot.subscribe(hikari.StartingEvent, self.client.start)
        self.bot.subscribe(hikari.StoppingEvent, self.client.stop)


        self.game_manager = game_manager

        self.guilds = []
        self.user_messages = {}
        self.leader_manager = LeaderManager()

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







    def add_commands(self):

        interactor = NominateLeaderInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(NominateLeaderInputBoundary, interactor)
        registry.register_value(LeaderManager, self.leader_manager)
        self.client.register(NominateLeaderCommand)

        interactor = CreateNewDraftInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(CreateNewDraftInputBoundary, interactor)
        self.client.register(CreateNewWhiteElephantDraftCommand)

        take_turn_interactor  = TakeTurnInteractor(self.game_manager)

        interactor = GetCurrentStateInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(GetCurrentStateInputBoundary, interactor)
        registry.register_value(LeaderManager, self.leader_manager)
        registry.register_value(TakeTurnInputBoundary, take_turn_interactor)
        self.client.register(GetCurrentStateCommand)


        interactor = FinishNominationsInteractor(self.game_manager)
        registry = self.client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
        registry.register_value(FinishNominationsInputBoundary, interactor)
        registry.register_value(TakeTurnInputBoundary, take_turn_interactor)
        registry.register_value(LeaderManager, self.leader_manager)
        self.client.register(FinishNominationsCommand)

        pass



