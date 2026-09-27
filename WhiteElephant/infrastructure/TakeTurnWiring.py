from WhiteElephant.infrastructure.LeaderPickMenu import LeaderPickMenu
from WhiteElephant.TakeTurn.TakeTurnPresenter import TakeTurnPresenter


def make_leader_pick_menu(next_user, data, input_boundary, leader_manager):
    return LeaderPickMenu(next_user, data, input_boundary, make_take_turn_presenter, leader_manager)


def make_take_turn_presenter(ctx, client, input_boundary, leader_manager):
    return TakeTurnPresenter(ctx, client, input_boundary, make_leader_pick_menu, leader_manager)