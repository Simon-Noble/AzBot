
import lightbulb

from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateOutputBoundary import GetCurrentStateOutputBoundary, \
    GetCurrentStateOutputData
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.infrastructure.DisplayHelpers import generate_pre_draft_display_message, \
    generate_draft_display_message
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.infrastructure.TakeTurnWiring import prompt_user_draft_pick


class GetCurrentStatePresenter(GetCurrentStateOutputBoundary):
    ctx: lightbulb.Context
    leader_manager: LeaderManager
    input_boundary: TakeTurnInputBoundary
    def __init__(self, ctx: lightbulb.Context, leader_manager: LeaderManager, input_boundary: TakeTurnInputBoundary) -> None:
        self.ctx = ctx
        self.leader_manager = leader_manager
        self.input_boundary = input_boundary

    async def present(self, output: GetCurrentStateOutputData) -> None:
        if not output.success:
            await self.ctx.respond(output.message)
            return
        if output.started:
            message = generate_draft_display_message(output, self.leader_manager)
            await self.ctx.respond(message)
            if output.prompt_current_player:
                await prompt_user_draft_pick(output, self.input_boundary, self.leader_manager, self.ctx)

            return
        else:
            message = generate_pre_draft_display_message(output, self.leader_manager)
            await self.ctx.respond(message)
        #        await self.ctx.respond(f"{icons} **{leader.name}** ({civs}) - nominated by {self.ctx.user.mention}".strip())




