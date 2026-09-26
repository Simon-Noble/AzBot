import lightbulb
from AzBot import AzBot
import json

from WhiteElephant.entities.GameManager import GameManager


def get_token() -> str:
    with open("token.json") as f:
        file = f.read()
        token = json.loads(file)["token"]
    return token


def main():

    game_manager = GameManager()

    bot = AzBot(get_token(), game_manager)



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

    bot.bot.run()


if __name__ == "__main__":
    main()
