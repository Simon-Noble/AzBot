import lightbulb

from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftInputBoundary import CreateNewDraftInputData, \
    CreateNewDraftInputBoundary
from WhiteElephant.DiscordCommands.CreateNewDraft.CreateNewDraftPresenter import CreateNewDraftPresenter


class CreateNewWhiteElephantDraftCommand(
    lightbulb.SlashCommand,
    name="create-new-white-elephant-draft",
    description="Create a new white elephant draft containing the desired memebers."
):

    member1 = lightbulb.user(
        f"member-1",
        "Member to be added",
        default=None
    )

    member2 = lightbulb.user(
        f"member-2",
        "Member to be added",
        default=None
    )

    member3 = lightbulb.user(
        f"member-3",
        "Member to be added",
        default=None
    )

    member4 = lightbulb.user(
        f"member-4",
        "Member to be added",
        default=None
    )

    member5 = lightbulb.user(
        f"member-5",
        "Member to be added",
        default=None
    )

    member6 = lightbulb.user(
        f"member-6",
        "Member to be added",
        default=None
    )

    member7 = lightbulb.user(
        f"member-7",
        "Member to be added",
        default=None
    )

    member8 = lightbulb.user(
        f"member-8",
        "Member to be added",
        default=None
    )

    member9 = lightbulb.user(
        f"member-9",
        "Member to be added",
        default=None
    )

    member10 = lightbulb.user(
        f"member-10",
        "Member to be added",
        default=None
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, input_boundary: CreateNewDraftInputBoundary) -> None:
        valid_memebers = []

        if self.member1 is not None:
            valid_memebers.append(self.member1.mention)
        if self.member2 is not None:
            valid_memebers.append(self.member2.mention)
        if self.member3 is not None:
            valid_memebers.append(self.member3.mention)
        if self.member4 is not None:
            valid_memebers.append(self.member4.mention)
        if self.member5 is not None:
            valid_memebers.append(self.member5.mention)
        if self.member6 is not None:
            valid_memebers.append(self.member6.mention)
        if self.member7 is not None:
            valid_memebers.append(self.member7.mention)
        if self.member8 is not None:
            valid_memebers.append(self.member8.mention)
        if self.member9 is not None:
            valid_memebers.append(self.member9.mention)
        if self.member10 is not None:
            valid_memebers.append(self.member10.mention)


        data = CreateNewDraftInputData(valid_memebers, f"{ctx.channel_id}")
        await input_boundary.execute(data, CreateNewDraftPresenter(ctx))

