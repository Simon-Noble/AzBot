import lightbulb

from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputData, \
    GetCurrentStateInputBoundary
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStatePresenter import GetCurrentStatePresenter
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.infrastructure.LeaderManager import LeaderManager

leaderManager = LeaderManager()



class GetCurrentStateCommand(
    lightbulb.SlashCommand,
    name="get-current-state",  # Discord command names must be lowercase
    description="Display The Current Draft State",
    ):
    prompt = lightbulb.boolean(
        "prompt",
        "Prompt the current player? (If applicable)",
        default=False,
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: GetCurrentStateInputBoundary, leader_manager: LeaderManager,
                     take_turn_input_boundary: TakeTurnInputBoundary,) -> None:



        data = GetCurrentStateInputData(f"{ctx.channel_id}", prompt_current_player=self.prompt)
        await input_boundary.execute(data, GetCurrentStatePresenter(ctx, leader_manager, take_turn_input_boundary))


