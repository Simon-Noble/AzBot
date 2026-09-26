import lightbulb

from WhiteElephant.CreateNewDraft.CreateNewDraftOutputBoundary import CreateNewDraftOutputBoundary, \
    CreateNewDraftOutputData


class CreateNewDraftPresenter(CreateNewDraftOutputBoundary):
    ctx: lightbulb.Context
    def __init__(self, ctx):
        self.ctx = ctx
    async def present(self, output: CreateNewDraftOutputData) -> None:

        await self.ctx.respond(output.message)

