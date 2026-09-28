import lightbulb

from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputData, \
    GetCurrentStateInputBoundary
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStatePresenter import GetCurrentStatePresenter
from WhiteElephant.infrastructure.LeaderManager import LeaderManager

leaderManager = LeaderManager()



class GetCurrentStateCommand(
    lightbulb.SlashCommand,
    name="get-current-state",  # Discord command names must be lowercase
    description="Display The Current Draft State",
):


    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: GetCurrentStateInputBoundary, leader_manager: LeaderManager) -> None:

        data = GetCurrentStateInputData(f"{ctx.channel_id}")
        await input_boundary.execute(data, GetCurrentStatePresenter(ctx, leader_manager))


