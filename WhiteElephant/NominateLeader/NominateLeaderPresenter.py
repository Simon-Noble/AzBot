import lightbulb

from WhiteElephant.NominateLeader.NominateLeaderOutputBoundary import NominateLeaderOutputBoundary, \
    NominateLeaderOutputData


class NominateLeaderPresenter(NominateLeaderOutputBoundary):
    _ctx: lightbulb.Context

    def __init__(self, ctx: lightbulb.Context):
        self.ctx = ctx

    async def present(self, output: NominateLeaderOutputData) -> None:
        if not output.success:
            await self.ctx.respond(output.message)
            return
        leader = output.leader
        icons = " ".join(filter(None, [leader.leader_emoji, leader.civ_emoji]))
        civs = leader.civ
        await self.ctx.respond(f"{icons} **{leader.name}** ({civs}) - nominated by {self.ctx.user.mention}".strip())