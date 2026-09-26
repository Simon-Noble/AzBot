import lightbulb

from WhiteElephant.infrastructure.Leader import Leader
from WhiteElephant.infrastructure.LeaderManager import LeaderManager
from WhiteElephant.NominateLeader.NominateLeaderInputBoundary import NominateLeaderInputBoundary, \
    NominateLeaderInputData
from WhiteElephant.NominateLeader.NominateLeaderPresenter import NominateLeaderPresenter

leaderManager = LeaderManager()


def _label(leader: Leader) -> str:
    return f"{leader.name} - {leader.civ}"

def resolve_leader(text: str) -> Leader | None:
    """Turn what the user submitted into a leader, or None if it isn't a valid leader."""
    allowed = {leader.id for leader in leaderManager.get_all_leaders()}
    exact = leaderManager.find(text)  # id, or an unambiguous name
    if exact and exact.id in allowed:
        return exact
    matches = leaderManager.search(text, limit=2)  # accept a partial name only if it's unambiguous
    return matches[0] if len(matches) == 1 else None

async def leader_autocomplete(ctx: lightbulb.AutocompleteContext[str]) -> None:
    query = str(ctx.focused.value or "")
    # (display text, value sent back when chosen)
    await ctx.respond([(_label(leader), leader.id) for leader in leaderManager.search(query, limit=15)])


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
    async def invoke(self, ctx: lightbulb.Context, input_boundary: NominateLeaderInputBoundary) -> None:
        leader = resolve_leader(self.leader)
        if leader is None:
            await ctx.respond(
                f"'{self.leader}' isn't a valid leader",
                ephemeral=True,
            )
            return



        data = NominateLeaderInputData(f"{ctx.user.mention}", leader, f"{ctx.channel_id}")

        await input_boundary.execute(data, NominateLeaderPresenter(ctx))


