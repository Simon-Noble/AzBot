from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsInputBoundary import FinishNominationsInputBoundary, \
    FinishNominationsInputData
from WhiteElephant.DiscordCommands.FinishNominations.FinishNominationsOutputBoundary import FinishNominationsOutputBoundary, \
    FinishNominationsOutputData
from WhiteElephant.entities.Game import DraftStartedException, SelectedGiftMismatchException
from WhiteElephant.entities.GameManager import GameManager, GameNotFoundException


class FinishNominationsInteractor(FinishNominationsInputBoundary):

    game_manager: GameManager

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    async def execute(self, data: FinishNominationsInputData, presenter: FinishNominationsOutputBoundary) -> None:
        try:
            game = self.game_manager.get_game(data.game_id)
        except GameNotFoundException:
            await presenter.present(FinishNominationsOutputData(success=False, message="Game not found"))
            return
        try:
            game.begin_draft()

            data = FinishNominationsOutputData(success=True, message="", users=game.users,
                                               nominated_leaders=game.nominated_gifts,
                                               started=game.draft_stared, turn_order=game.turn_order,
                                               current_assignments=game.current_assignment,
                                               unselected_leaders=game.unselected_gifts,
                                               stolen_leaders=game.gift_times_stolen,
                                               stolen_picks=game.user_times_stolen,
                                               user_nominated_leaders=game.user_nominated_gifts,
                                               current_chain=game.current_chain)
        except DraftStartedException as e:
            data = FinishNominationsOutputData(success=False, message="The draft has already started.")
        except SelectedGiftMismatchException as e:
            data = FinishNominationsOutputData(success=False, message=f"{e}")

        await presenter.present(data)
