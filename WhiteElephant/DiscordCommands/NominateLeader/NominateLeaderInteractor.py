from WhiteElephant.DiscordCommands.NominateLeader.NominateLeaderOutputBoundary import NominateLeaderOutputBoundary, \
    NominateLeaderOutputData
from WhiteElephant.entities.Game import DraftStartedException, TooManyGiftsException, DuplicateGiftException
from WhiteElephant.entities.GameManager import GameManager, GameNotFoundException
from WhiteElephant.DiscordCommands.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary, \
    NominateLeaderInputData


class NominateLeaderInteractor(NominateLeaderInputBoundary):
    game_manager: GameManager

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    async def execute(self, data: NominateLeaderInputData, presenter: NominateLeaderOutputBoundary) -> None:

        try:
            game = self.game_manager.get_game(data.game_id)
        except GameNotFoundException:
            await presenter.present(NominateLeaderOutputData(success=False, message="Game not found"))
            return

        try:
            game.add_gift_to_pool(data.user, data.leader_id)
        except DraftStartedException:

            await presenter.present(NominateLeaderOutputData(success=False, message="Draft started", leader=None))
            return
        except TooManyGiftsException as e:
            await presenter.present(NominateLeaderOutputData(success=False, message=f"{data.user} has already selected "
                                                                                    f"2 leaders", leader=None))

            return
        except DuplicateGiftException:
            await presenter.present(NominateLeaderOutputData(success=False, message=f"{data.leader_id} has already been "
                                                                                    f"selected", leader=data.leader_id))
            return

        await presenter.present(NominateLeaderOutputData(success=True, message="Successfully nominated leader",
                                                         leader=data.leader_id))




