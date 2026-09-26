import lightbulb

from WhiteElephant.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputData, \
    GetCurrentStateInputBoundary
from WhiteElephant.GetCurrentState.GetCurrentStatePresenter import GetCurrentStatePresenter
from WhiteElephant.infrastructure.Leader import Leader
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary, \
    NominateLeaderInputData
from WhiteElephant.NominateLeader.NominateLeaderPresenter import NominateLeaderPresenter

leaderManager = LeaderManager()



class GetCurrentState(
    lightbulb.SlashCommand,
    name="get-current-state",  # Discord command names must be lowercase
    description="Display The Current Draft State",
):


    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: GetCurrentStateInputBoundary) -> None:

        data = GetCurrentStateInputData(f"{ctx.channel_id}")
        await input_boundary.execute(data, GetCurrentStatePresenter(ctx))


