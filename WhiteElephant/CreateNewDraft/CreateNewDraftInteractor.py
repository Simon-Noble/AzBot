from WhiteElephant.CreateNewDraft.CreateNewDraftInputBoundary import CreateNewDraftInputBoundary, \
    CreateNewDraftInputData
from WhiteElephant.CreateNewDraft.CreateNewDraftOutputBoundary import CreateNewDraftOutputBoundary, \
    CreateNewDraftOutputData
from WhiteElephant.entities.GameManager import GameManager


class CreateNewDraftInteractor(CreateNewDraftInputBoundary):
    game_manager: GameManager

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    async def execute(self, data: CreateNewDraftInputData, presenter: CreateNewDraftOutputBoundary) -> None:
        if len(data.users) < 1:
            await presenter.present(CreateNewDraftOutputData(success=False, message="Please select at least one user."))
            return


        self.game_manager.create_game(data.users, data.game_id)

        await presenter.present(CreateNewDraftOutputData(success=True, message="Draft successfully created. with"
                                                                               f"users {data.users} in channel {data.game_id}"))

