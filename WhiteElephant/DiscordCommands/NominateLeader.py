import lightbulb

from WhiteElephant.infrastructure.Leader import Leader
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary, \
    NominateLeaderInputData
from WhiteElephant.NominateLeader.NominateLeaderPresenter import NominateLeaderPresenter


def _label(leader: Leader) -> str:
    return f"{leader.name} - {leader.civ}"

def resolve_leader(text: str, leader_manager: LeaderManager) -> Leader | None:
    """Turn what the user submitted into a leader, or None if it isn't a valid leader."""
    allowed = {leader.id for leader in leader_manager.get_all_leaders()}
    exact = leader_manager.find(text)  # id, or an unambiguous name
    if exact and exact.id in allowed:
        return exact
    matches = leader_manager.search(text, limit=2)  # accept a partial name only if it's unambiguous
    return matches[0] if len(matches) == 1 else None

async def leader_autocomplete(ctx: lightbulb.AutocompleteContext[str], leader_manager: LeaderManager) -> None:
    query = str(ctx.focused.value or "")
    # (display text, value sent back when chosen)
    await ctx.respond([(_label(leader), leader.id) for leader in leader_manager.search(query, limit=15)])


class NominateLeader(
    lightbulb.SlashCommand,
    name="nominateleader",  # Discord command names must be lowercase
    description="Nominate a Civilization VI leader",
):
    leader = lightbulb.string(
        "leader",
        "Start typing a leader or civilization name",
        autocomplete=leader_autocomplete
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: NominateLeaderInputBoundary, leader_manager: LeaderManager) -> None:
        leader = resolve_leader(self.leader, leader_manager)
        if leader is None:
            await ctx.respond(
                f"'{self.leader}' isn't a valid leader",
                ephemeral=True,
            )
            return



        data = NominateLeaderInputData(f"{ctx.user.mention}", leader.id, f"{ctx.channel_id}")

        await input_boundary.execute(data, NominateLeaderPresenter(ctx,leader_manager))


