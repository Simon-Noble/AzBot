from WhiteElephant.TakeTurn.TakeTurnInputBoundary import TakeTurnInputBoundary, TakeTurnInputData
from WhiteElephant.TakeTurn.TakeTurnOutputBoundary import TakeTurnOutputBoundary, TakeTurnOutputData
from WhiteElephant.entities.Game import DraftStartedException, OutOfOrderException, TooManyStealsException, \
    TooManyGiftsException
from WhiteElephant.entities.GameManager import GameManager, GameNotFoundException


class TakeTurnInteractor(TakeTurnInputBoundary):


    game_manager: GameManager
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    async def execute(self, data: TakeTurnInputData, presenter: TakeTurnOutputBoundary) -> None:
        print("success")

        try:
            game = self.game_manager.get_game(data.game_id)
        except GameNotFoundException:
            await presenter.present(TakeTurnOutputData(success=False, message="Game not found"))
            return

        if not data.steal:
            try:
                game.draw_from_pool(data.user)

                data = TakeTurnOutputData(success=True, message="", users=game.users,
                                          nominated_leaders=game.nominated_gifts,
                                          started=game.draft_stared, turn_order=game.turn_order,
                                          current_assignments=game.current_assignment,
                                          unselected_leaders=game.unselected_gifts,
                                          stolen_leaders=game.gift_times_stolen,
                                          stolen_picks=game.user_times_stolen,
                                          user_nominated_leaders=game.user_nominated_gifts,
                                          current_chain=game.current_chain)
            except DraftStartedException as e:
                data = TakeTurnOutputData(success=False, message="The draft has not started yet.")
            except OutOfOrderException as e:
                data = TakeTurnOutputData(success=False, message="It is not your turn.")
            except TooManyGiftsException:
                data = TakeTurnOutputData(success=False, message=f"You have too many leaders")
            await presenter.present(data)
            return
        try:
            game.steal_gift(data.user, data.leader_to_steal)
            data = TakeTurnOutputData(success=True, message="", users=game.users,
                                      nominated_leaders=game.nominated_gifts,
                                      started=game.draft_stared, turn_order=game.turn_order,
                                      current_assignments=game.current_assignment,
                                      unselected_leaders=game.unselected_gifts,
                                      stolen_leaders=game.gift_times_stolen,
                                      stolen_picks=game.user_times_stolen,
                                      user_nominated_leaders=game.user_nominated_gifts,
                                      current_chain=game.current_chain)
        except DraftStartedException as e:
            data = TakeTurnOutputData(success=False, message="The draft has not started yet.")
        except OutOfOrderException as e:
            data = TakeTurnOutputData(success=False, message="It is not your turn.")
        except TooManyStealsException as e:
            data = TakeTurnOutputData(success=False, message=f"{e}")
        except TooManyGiftsException:
            data = TakeTurnOutputData(success=False, message=f"You have too many leaders")

        await presenter.present(data)
        return


