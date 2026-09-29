import lightbulb

from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsOutputBoundary import FinishNominationsOutputData, \
    FinishNominationsOutputBoundary
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.infrastructure import DisplayHelpers
from WhiteElephant.infrastructure.DisplayHelpers import generate_draft_display_message
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.infrastructure.LeaderPickMenu import LeaderPickMenu

from WhiteElephant.infrastructure.TakeTurnWiring import make_take_turn_presenter, prompt_user_draft_pick


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
        await self.ctx.respond(generate_draft_display_message(data, self.leader_manager))

        await prompt_user_draft_pick(data, self.take_turn_input_boundary, self.leader_manager, self.ctx)


