
from lightbulb.ext import tasks
from AzBot import *
import json


def get_token() -> str:
    with open("token.json") as f:
        file = f.read()
        token = json.loads(file)["token"]
    return token


def main():

    bot = AzBot(
        token=get_token()
    )

    lightbulb.ext.tasks.load(bot)

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

    bot.run()


if __name__ == "__main__":
    main()
