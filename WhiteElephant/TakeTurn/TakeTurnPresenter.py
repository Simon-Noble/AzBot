from typing import Callable

import lightbulb
from lightbulb.components import MenuContext

from WhiteElephant.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.TakeTurn.TakeTurnOutputBoundary import TakeTurnOutputBoundary, TakeTurnOutputData
from WhiteElephant.infrastructure import DisplayHelpers
from WhiteElephant.infrastructure.LeaderManager import LeaderManager

MenuFactory = Callable[[str, TakeTurnOutputData, TakeTurnInputBoundary, LeaderManager], lightbulb.components.Menu]

class TakeTurnPresenter(TakeTurnOutputBoundary):

    ctx: MenuContext
    client: lightbulb.Client
    input_boundary: TakeTurnInputBoundary
    menu_factory: MenuFactory
    leader_manager: LeaderManager

    def __init__(self, ctx: MenuContext, client: lightbulb.Client, input_boundary: TakeTurnInputBoundary,
                 menu_factory: MenuFactory, leader_manager: LeaderManager) -> None:
        self.ctx = ctx
        self.client = client
        self.input_boundary = input_boundary
        self.menu_factory = menu_factory
        self.leader_manager = leader_manager

    async def present(self, data: TakeTurnOutputData) -> None:
        if not data.success:
            await self.ctx.respond(data.message)
            return


        await self.ctx.respond(DisplayHelpers.generate_draft_display_message(data, self.leader_manager))
        if len(data.turn_order)>0:
            menu = self.menu_factory(data.turn_order[0], data, self.input_boundary, self.leader_manager)
            await self.ctx.respond("Pick a leader:", components=menu, ephemeral=False)
            await menu.attach(self.client, timeout=None)
