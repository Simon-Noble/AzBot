
import lightbulb

from WhiteElephant.GetCurrentState.GetCurrentStateOutputBoundary import GetCurrentStateOutputBoundary, \
    GetCurrentStateOutputData


class GetCurrentStatePresenter(GetCurrentStateOutputBoundary):
    ctx: lightbulb.Context
    def __init__(self, ctx: lightbulb.Context):
        self.ctx = ctx

    async def present(self, output: GetCurrentStateOutputData) -> None:
        if not output.success:
            await self.ctx.respond(output.message)
            return
        if output.started:
            message = (f"Draft is ongoing:"
                       f"\nCurrent draft order: {output.turn_order}")
            return
        else:
            message = f"Current Leader Selections:"
            for user in output.users:

                leaders = output.user_nominated_leaders[user]
                message += f"\n"
                for leader in leaders:
                    icons = " ".join(filter(None, [leader.leader_emoji, leader.civ_emoji]))
                    civs = leader.civ
                    message += f"{icons} **{leader.name}** ({civs})  "
                message += f"- nominated by {user}"
            message +=f"\nDraft can start once each user has nominated 2 leaders"
            await self.ctx.respond(message)
        #        await self.ctx.respond(f"{icons} **{leader.name}** ({civs}) - nominated by {self.ctx.user.mention}".strip())
