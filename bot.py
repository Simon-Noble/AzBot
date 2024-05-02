import lightbulb
from lightbulb.ext import tasks
from AzBot import AzBot
import json

from UseCase.TalkingTracker.TalkingTracker import TalkingTracker
from UseCase.TypingTracker.TypingTracker import TypingTracker
from WriteToFileTextOutputBoundary import WriteToFileTextOutputBoundary


def get_token() -> str:
    with open("token.json") as f:
        file = f.read()
        token = json.loads(file)["token"]
    return token


def main():

    with open("Typing_Time.txt") as f:
        typing_file = f.read()
        starting_typing = json.loads(typing_file)
    typing_output_boundary = WriteToFileTextOutputBoundary("Typing_Time.txt")
    typing_tracker = TypingTracker(typing_output_boundary, starting_typing)

    with open("Talking_Time.txt") as f:
        talking_file = f.read()
        starting_talking = json.loads(talking_file)
    talking_output_boundary = WriteToFileTextOutputBoundary("Talking_Time.txt")
    talking_tracker = TalkingTracker(talking_output_boundary, starting_talking)

    Azbot = AzBot(get_token(), typing_tracker, talking_tracker
    )

    lightbulb.ext.tasks.load(Azbot.bot)

    """
    @bot.command()
    @lightbulb.command("group", "this is a group")
    @lightbulb.implements(lightbulb.SlashCommandGroup)
    async def my_group(ctx):
        pass
    
    
    @my_group.child
    @lightbulb.command("subcommand", "this is a subcommand")
    @lightbulb.implements(lightbulb.SlashSubCommand)
    async def subcommand(ctx):
        await ctx.respond("i am a subcommand")
    
    """

    Azbot.bot.run()


if __name__ == "__main__":
    main()
