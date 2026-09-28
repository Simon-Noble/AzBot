import lightbulb

from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsOutputBoundary import FinishNominationsOutputData, \
    FinishNominationsOutputBoundary
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.infrastructure import DisplayHelpers
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.infrastructure.LeaderPickMenu import LeaderPickMenu

from WhiteElephant.infrastructure.TakeTurnWiring import make_take_turn_presenter



class FinishNominationsPresenter(FinishNominationsOutputBoundary):

    ctx: lightbulb.Context
    client: lightbulb.Client
    take_turn_input_boundary: TakeTurnInputBoundary
    leader_manager: LeaderManager

    def __init__(self, ctx: lightbulb.Context, client: lightbulb.Client, take_turn_input_boundary: TakeTurnInputBoundary,
                 leader_manager: LeaderManager) -> None:
        self.ctx = ctx
        self.client = client
        self.take_turn_input_boundary = take_turn_input_boundary
        self.leader_manager = leader_manager

    async def present(self, data: FinishNominationsOutputData) -> None:
        if not data.success:
            await self.ctx.respond(data.message)
            return
        await self.ctx.respond(DisplayHelpers.generate_draft_display_message(data, self.leader_manager))

        menu = LeaderPickMenu(data.turn_order[0], data, self.take_turn_input_boundary,
                              make_take_turn_presenter, self.leader_manager)
        await self.ctx.respond("Pick a leader:", components=menu, ephemeral=True )
        await menu.attach(self.client, timeout=None)
        pass