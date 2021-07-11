import asyncio
import discord
from discord.ext import commands
import random
from GameLogic import Game

intents = discord.Intents.default()
intents.members = True


Client = discord.Client()
client = commands.Bot(command_prefix="!", intents=intents)

GAME_CATEGORY = 863371910465191947


@client.event
async def on_ready():
    print(
        f"Bot ready! Running version {str(discord.__version__)} Have fun exploding kittens!")


@client.command()
async def start(ctx):
    # startup functions
    voice_channel = ctx.author.voice.channel
    game_category = client.get_channel(GAME_CATEGORY)
    players = voice_channel.members
    game_channels = await create_voice_channels(players, game_category)
    game = Game(len(players), len(players) - 1)
    queue = players.copy()
    random.shuffle(queue)
    queue_dict = {p: h for p, h in zip(queue, game.players)}
    await do_turn(queue, queue_dict, game_channels)


async def add_reactions(player, hand, game_channel):
    pass


async def show_hand(player, hand, game_channel):
    await game_channel.send(hand)


async def do_turn(queue, queue_dict, game_channels):

    for player in queue:
        await show_hand(player, queue_dict[player], game_channels[player])
    current_player = queue[0]
    add_card_reactions(current_player, queue_dict[current_player])


async def create_voice_channels(members, game_category):
    game_channels = {}
    print(game_category)
    for member in members:
        for channel in game_category.channels:
            if channel.permissions_for(member).view_channel:
                game_channels[member] = channel
                break
        else:
            overwrites = {
                game_category.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            game_channels[member] = await game_category.create_text_channel(member.display_name, overwrites=overwrites)
    return game_channels


@client.event
async def on_raw_reaction_add(payload):
    user = payload.member
    if user.bot:
        return

    emoji = str(payload.emoji)
    reaction_channel = client.get_channel(payload.channel_id)
    # reaction_guild = client.get_guild(payload.guild_id)
    # reaction_message = await reaction_channel.fetch_message(payload.message_id)
    if emoji == '🐢':
        await reaction_channel.send("TOORTOOLE")

with open("token.txt", "r") as token_file:
    token = token_file.readline()
    client.run(token)
