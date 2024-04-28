import lightbulb
from lightbulb.ext import tasks
import random
from AzBot import *
import json


def get_token() -> str:
    with open("token.json") as f:
        file = f.read()
        token = json.loads(file)["token"]
    return token


bot = AzBot(
    token=get_token()
)

lightbulb.ext.tasks.load(bot)


@bot.listen(hikari.StartedEvent)
async def on_start(event: hikari.events.lifetime_events.StartedEvent):
    print("bot started")
    print(event)
    guilds = bot.rest.fetch_my_guilds()
    async for item in guilds:
        bot.guilds.append(item)
        bot.full_power[item.id] = False
    print(bot.guilds)
    print(bot.full_power)


"""
@bot.listen(hikari.GuildJoinEvent)
async def join_guild(event: hikari.events.guild_events.GuildJoinEvent):
    print(type(event))
    guild = event.get_guild()

    new_category = await guild.create_category(name="Azcanta Land", position=3, reason="Azcanta's Home", )
    print(new_category.position)
    new_channel = await guild.create_text_channel(name="Azcanta's Lair", category=new_category)
"""


@bot.listen(hikari.GuildTypingEvent)
async def typing_tracker(event: hikari.events.typing_events.GuildTypingEvent):
    if bot.full_power[event.guild_id]:
        user = await bot.rest.fetch_user(event.user_id)
        await bot.rest.create_message(channel=event.channel_id, content="Please stop typing " + user.mention,
                                      user_mentions=[event.user_id]
                                      )


@bot.listen(hikari.GuildMessageCreateEvent)
async def message_response(event: hikari.events.message_events.GuildMessageCreateEvent):
    if not event.author.is_bot:
        print(f"Author: {event.author} | Content:{str(event.content)} \n"
              f"Author_id: {event.author_id} | Guild: {event.get_guild()}")




@bot.command()
@lightbulb.command('fullpower', 'fullpower')
@lightbulb.implements(lightbulb.SlashCommand)
async def activate_full_power(ctx: lightbulb.context.slash.SlashContext):
    await ctx.respond("Full power activated, typing is no longer allowed")
    bot.full_power[ctx.guild_id] = True
    print(bot.full_power)


@bot.command()
@lightbulb.command('lowpower', 'lowpower')
@lightbulb.implements(lightbulb.SlashCommand)
async def activate_full_power(ctx: lightbulb.context.slash.SlashContext):
    await ctx.respond("Full power de-activated, typing is now allowed")
    bot.full_power[ctx.guild_id] = False
    print(bot.full_power)



@bot.command()
@lightbulb.option("graphics", "Does the game have good graphics (good style counts) (0-100)",
                  type=int, min_value=1, max_value=100)
@lightbulb.option("fun", "Is the game fun (0-100)", type=int, min_value=1, max_value=100)
@lightbulb.option("functionality", "Does the game function well (0-100)", type=int, min_value=1, max_value=100)
@lightbulb.option("themes", "Does this game have good themes or story elements? (0-100)", type=int,
                  min_value=1, max_value=100)
@lightbulb.option("gameplay", "Does this game have good gameplay? (0-100)", type=int, min_value=1, max_value=100)
@lightbulb.option("influence", "Does this game have wide influence? (0-100)", type=int, min_value=1, max_value=100)
@lightbulb.option("genre_exemplar", "Is this a good game in it's genre? (0-100)", type=int, min_value=1, max_value=100)
@lightbulb.option("name", "What is the name of this game on wikipedia?", type=str)
@lightbulb.command("rate_game", "rate a video game!")
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.context.slash.SlashContext):
    save_string = ("\n" +
                   str(ctx.options.name) + "|" + str(ctx.options.genre_exemplar) + "|" + str(ctx.options.influence) +
                   "|" + str(ctx.options.gameplay) + "|" + str(ctx.options.themes) + "|" + str(
                ctx.options.functionality) +
                   "|" + str(ctx.options.fun) + "|" + str(ctx.options.graphics) + "|" + str(ctx.author)
                   )

    print(save_string)
    f = open("gameRatings\AzBot.txt", "a")
    f.write(save_string)
    f.close()

    await ctx.respond("Thank you for rating " + str(ctx.options.name))


@bot.command()
@lightbulb.command("square_game", "Commands for the RedSquare BlueSquare game!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def square_game(ctx):
    pass


@square_game.child
@lightbulb.option("difficulty", "How hard should the game be (1-4)", type=int, min_value=1, max_value=4)
@lightbulb.command('new_game', 'Create a new game of RedSquare BlueSquare')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def new_game(ctx: lightbulb.context.slash.SlashContext):
    difficulty_settings: dict[int:list[int]] = {1: [4, 4, 4], 2: [6, 6, 8], 3: [7, 7, 11], 4: [9, 9, 17]}

    difficulty = difficulty_settings[ctx.options.difficulty]
    game = bot.get_game(ctx.author.id)

    game.new_game(difficulty[0], difficulty[1], difficulty[2])
    await ctx.respond(game.discord_display())
    print(game.discord_display())


@square_game.child
@lightbulb.option("y", "y position of the tile to switch", type=int, min_value=1)
@lightbulb.option("x", "x position of the tile to switch", type=int, min_value=1)
@lightbulb.command('take_turn', 'Take a turn with the given co-ordinates')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def take_turn(ctx: lightbulb.context.slash.SlashContext):
    if ctx.author.id in bot.tent_games:
        game = bot.get_game(ctx.author.id)

        if ctx.options.x - 1 > game.get_board().get_width() or ctx.options.y - 1 > game.get_board().get_height():
            await ctx.respond("Please pick a valid position")
        else:
            if not game.get_board().object_at(ctx.options.x - 1, ctx.options.y - 1).get_char() == "r":
                # swap the tile on that space
                game.get_board().switch_type(ctx.options.x - 1, ctx.options.y - 1)

                if game.get_board().check_game_won():
                    await ctx.respond("Congratulations! You win! \n Here is the final board: \n" +
                                      game.discord_display())
                else:
                    await ctx.respond(game.discord_display())

            else:
                await ctx.respond("Green tiles can not be changed, pick a different tile.")

    else:
        await ctx.respond("No game found, try /new_game")


@square_game.child
@lightbulb.command('see_board', 'See your current board')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def see_board(ctx: lightbulb.context.slash.SlashContext):
    if ctx.author.id in bot.tent_games:
        await ctx.respond(bot.get_game(ctx.author.id).discord_display())
    else:
        await ctx.respond("No game found, try /new_game")


@square_game.child
@lightbulb.command('rules', 'Explain the rules for SquareGame')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def see_rules(ctx: lightbulb.context.slash.SlashContext):
    await ctx.respond("This is a puzzle game in which you have a board of Green squares, Empty squares, and Numbers "
                      "on the top \nThe goal is to create Red squares such that each Green square has a Red square"
                      "paired to it, and that no Red square is touching another Red square \nGreen squares must "
                      "have an adjacent Red square (cardinal directions) but Red squares must not touch another"
                      "Red adjacent square (including diagonals) \nThe numbers on the top and side say how many"
                      "Red squares are in each row and column respectively. \nThe game is completed once each green"
                      "square has a red square touching it, (1 Red to 1 Green) no Red squares are touching, and"
                      "each number on the top and sides has the correct number of Red squares. \nBlue and black"
                      "squares have no impact on the game, but are useful for keeping track of where Red squares"
                      "can not be. here is an example solved board: \n \n:blue_square::zero::one:\n"
                      ":zero::blue_square::blue_square:\n"
                      ":one::green_square::red_square:")


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
