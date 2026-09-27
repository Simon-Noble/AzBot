import lightbulb

from WhiteElephant.FinishNominations.FinishNominationsInputBoundary import FinishNominationsInputBoundary, \
    FinishNominationsInputData
from WhiteElephant.FinishNominations.FinishNominationsPresenter import FinishNominationsPresenter
from WhiteElephant.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary

from WhiteElephant.infrastructure.LeaderManager import LeaderManager


class FinishNominations(
    lightbulb.SlashCommand,
    name="finish-nominations",  # Discord command names must be lowercase
    description="Finish nomination period and begin the draft",
):


    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: FinishNominationsInputBoundary, client: lightbulb.Client,
                     take_turn_input_boundary: TakeTurnInputBoundary,
                     leader_manager: LeaderManager) -> None:

        data = FinishNominationsInputData(f"{ctx.channel_id}")
        await input_boundary.execute(data, FinishNominationsPresenter(ctx, client, take_turn_input_boundary, leader_manager))


