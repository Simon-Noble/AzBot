import lightbulb

from WhiteElephant.NominateLeader.NominateLeaderOutputBoundary import NominateLeaderOutputBoundary, \
    NominateLeaderOutputData
from WhiteElephant.infrastructure.LeaderManager import LeaderManager


class NominateLeaderPresenter(NominateLeaderOutputBoundary):
    _ctx: lightbulb.Context
    leader_manager: LeaderManager

    def __init__(self, ctx: lightbulb.Context, leader_manager: LeaderManager):
        self.ctx = ctx
        self.leader_manager = leader_manager

    async def present(self, output: NominateLeaderOutputData) -> None:
        if not output.success:
            await self.ctx.respond(output.message)
            return
        leader_id = output.leader
        icons = " ".join(filter(None, [self.leader_manager.BY_ID[leader_id].leader_emoji,
                                       self.leader_manager.BY_ID[leader_id].civ_emoji]))
        civs = self.leader_manager.BY_ID[leader_id].civ
        await self.ctx.respond(f"{icons} **{self.leader_manager.BY_ID[leader_id].name}** ({civs}) - nominated by "
                               f"{self.ctx.user.mention}".strip(), ephemeral=True)