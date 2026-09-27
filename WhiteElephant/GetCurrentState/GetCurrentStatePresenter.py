
import lightbulb

from WhiteElephant.GetCurrentState.GetCurrentStateOutputBoundary import GetCurrentStateOutputBoundary, \
    GetCurrentStateOutputData
from WhiteElephant.infrastructure.DisplayHelpers import generate_pre_draft_display_message, \
    generate_draft_display_message
from WhiteElephant.infrastructure.LeaderManager import LeaderManager


class GetCurrentStatePresenter(GetCurrentStateOutputBoundary):
    ctx: lightbulb.Context
    leader_manager: LeaderManager
    def __init__(self, ctx: lightbulb.Context, leader_manager: LeaderManager) -> None:
        self.ctx = ctx
        self.leader_manager = leader_manager

    async def present(self, output: GetCurrentStateOutputData) -> None:
        if not output.success:
            await self.ctx.respond(output.message)
            return
        if output.started:
            message = generate_draft_display_message(output, self.leader_manager)
            await self.ctx.respond(message)

            return
        else:
            message = generate_pre_draft_display_message(output, self.leader_manager)
            await self.ctx.respond(message)
        #        await self.ctx.respond(f"{icons} **{leader.name}** ({civs}) - nominated by {self.ctx.user.mention}".strip())




