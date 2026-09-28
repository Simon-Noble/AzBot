
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateInputBoundary import GetCurrentStateInputBoundary, \
    GetCurrentStateInputData
from WhiteElephant.DiscordCommands.GetCurrentState.GetCurrentStateOutputBoundary import GetCurrentStateOutputBoundary, \
    GetCurrentStateOutputData
from WhiteElephant.entities.GameManager import GameManager, GameNotFoundException


class GetCurrentStateInteractor(GetCurrentStateInputBoundary):


    game_manager: GameManager
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    async def execute(self, data: GetCurrentStateInputData, presenter: GetCurrentStateOutputBoundary) -> None:
        try:
            game = self.game_manager.get_game(data.game_id)
        except GameNotFoundException:
            await presenter.present(GetCurrentStateOutputData(success=False, message="Game not found"))
            return

        data = GetCurrentStateOutputData(success=True, message="", users= game.users,
                                         nominated_leaders=game.nominated_gifts,
                                         started=game.draft_stared, turn_order= game.turn_order,
                                         current_assignments= game.current_assignment,
                                         unselected_leaders= game.unselected_gifts,
                                         stolen_leaders=game.gift_times_stolen,
                                         stolen_picks=game.user_times_stolen,
                                         user_nominated_leaders=game.user_nominated_gifts,
                                         current_chain= game.current_chain)
        await presenter.present(data)
