import lightbulb

from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftOutputBoundary import CreateNewDraftOutputBoundary, \
    CreateNewDraftOutputData


class CreateNewDraftPresenter(CreateNewDraftOutputBoundary):
    ctx: lightbulb.Context
    def __init__(self, ctx):
        self.ctx = ctx
    async def present(self, output: CreateNewDraftOutputData) -> None:
        message= output.message
        await self.ctx.respond(message, ephemeral=True)

