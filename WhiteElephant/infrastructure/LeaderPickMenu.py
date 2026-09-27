from typing import Callable

import lightbulb

from WhiteElephant.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary, TakeTurnInputData
from WhiteElephant.TakeTurn.TakeTurnOutputBoundary import TakeTurnOutputBoundary
from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData
from WhiteElephant.infrastructure.LeaderManager import LeaderManager

PresenterFactory = Callable[[lightbulb.components.MenuContext, lightbulb.Client, TakeTurnInputBoundary, LeaderManager], TakeTurnOutputBoundary]


class LeaderPickMenu(lightbulb.components.Menu):
    def __init__(self, next_user: str, data: GenericStateOutputData, input_boundary: TakeTurnInputBoundary,
                 presenter_factory: PresenterFactory, leader_manager: LeaderManager) -> None:
        self.next_user = next_user
        self.leaders_by_id = {str(f.id): f for f in data.nominated_leaders}
        self.input_boundary = input_boundary
        self.presenter_factory = presenter_factory
        self.leader_manager = leader_manager

        options = [
            lightbulb.components.TextSelectOption(
                label=self.leader_manager.BY_ID[leader_id].name,
                value=str(leader_id),
                description=f"Steal {self.leader_manager.BY_ID[leader_id].name} from {user}"
            )
            for user in data.current_assignments for leader_id in data.current_assignments[user]
            if leader_id is not None and leader_id not in data.current_chain and user != self.next_user
        ]
        if len(data.unselected_leaders) > 0:
            options.append(lightbulb.components.TextSelectOption(
                label="draw",
                value=str("draw"),
                description="Get a new random leader"
            ))
        self.select = self.add_text_select(options, self.on_select, placeholder="Choose a leader...")

    async def predicate(self, ctx: lightbulb.components.MenuContext) -> bool:
        if ctx.user.mention != self.next_user:
            await ctx.respond(f"This menu isn't for you, it is for {self.next_user}", ephemeral=True)
            return False
        return True

    async def on_select(self, ctx: lightbulb.components.MenuContext) -> None:
        (leader_id,) = ctx.selected_values_for(self.select)
        presenter = self.presenter_factory(ctx, ctx.client, self.input_boundary, self.leader_manager)

        if leader_id =="draw":
            await self.input_boundary.execute(TakeTurnInputData(str(ctx.channel_id), False, ctx.user.mention),
                                              presenter)
            return
        else:
            leader = self.leaders_by_id[leader_id]
            await self.input_boundary.execute(TakeTurnInputData(str(ctx.channel_id),True, ctx.user.mention,
                                                                leader_to_steal= leader),
                                              presenter)
            return



