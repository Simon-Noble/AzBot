from typing import Callable, Awaitable

import lightbulb
from lightbulb.components import MenuContext

from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnOutputBoundary import TakeTurnOutputBoundary, TakeTurnOutputData
from WhiteElephant.infrastructure import DisplayHelpers
from WhiteElephant.infrastructure.LeaderManager import LeaderManager

MenuFactory = Callable[[str, TakeTurnOutputData, TakeTurnInputBoundary, LeaderManager], lightbulb.components.Menu]
PromptNextPick = Callable[[TakeTurnOutputData, TakeTurnInputBoundary, LeaderManager, lightbulb.Context], Awaitable[None]]

class TakeTurnPresenter(TakeTurnOutputBoundary):

    ctx: MenuContext
    client: lightbulb.Client
    input_boundary: TakeTurnInputBoundary
    menu_factory: MenuFactory
    leader_manager: LeaderManager
    prompt_next_pick: PromptNextPick


    def __init__(self, ctx: MenuContext, client: lightbulb.Client, input_boundary: TakeTurnInputBoundary,
                 menu_factory: MenuFactory, leader_manager: LeaderManager, prompt_next_pick: PromptNextPick) -> None:
        self.ctx = ctx
        self.client = client
        self.input_boundary = input_boundary
        self.menu_factory = menu_factory
        self.leader_manager = leader_manager
        self.prompt_next_pick = prompt_next_pick

    async def present(self, data: TakeTurnOutputData) -> None:
        if not data.success:
            await self.ctx.respond(data.message)
            return


        await self.ctx.respond(DisplayHelpers.generate_draft_display_message(data, self.leader_manager))
        if len(data.turn_order)>0:
            await self.prompt_next_pick(data, self.input_boundary, self.leader_manager, self.ctx)
