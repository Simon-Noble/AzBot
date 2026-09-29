import lightbulb

from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary
from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.infrastructure.LeaderPickMenu import LeaderPickMenu
from WhiteElephant.DiscordCommands.TakeTurn.TakeTurnPresenter import TakeTurnPresenter


def make_leader_pick_menu(next_user, data, input_boundary, leader_manager):
    return LeaderPickMenu(next_user, data, input_boundary, make_take_turn_presenter, leader_manager)


def make_take_turn_presenter(ctx, client, input_boundary, leader_manager):
    return TakeTurnPresenter(ctx, client, input_boundary, make_leader_pick_menu, leader_manager, prompt_user_draft_pick)


async def prompt_user_draft_pick(data: GenericStateOutputData, take_turn_input_boundary: TakeTurnInputBoundary,
                                 leader_manager: LeaderManager,
                                 ctx: lightbulb.Context | lightbulb.MenuContext) -> None:

    menu = make_leader_pick_menu(data.turn_order[0], data, take_turn_input_boundary,
                          leader_manager)
    await ctx.respond(f"{data.turn_order[0]}, pick a leader:", components=menu, ephemeral=False,
                           user_mentions=True)
    await menu.attach(ctx.client, timeout=None)