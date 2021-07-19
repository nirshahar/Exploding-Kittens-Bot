import asyncio
import discord
from discord.ext import commands
import random
from GameLogic import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
GAME_CATEGORY = 863371910465191947

players_dict = None
game = None


@client.event
async def on_ready():
    print(
        f"Bot ready! Running version {str(discord.__version__)} Have fun exploding kittens!")


async def create_voice_channels(members, game_category):
    game_channels = {}
    for member in members:
        for channel in game_category.channels:
            if channel.name == member.name:
                game_channels[member] = channel
                break
            # if channel.permissions_for(member).view_channel and channel.name:
            #     game_channels[member] = channel
            #     break
        else:
            overwrites = {
                game_category.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            game_channels[member] = await game_category.create_text_channel(member.name, overwrites=overwrites)
    return game_channels


async def do_turn(game: Game):
    for player in game.players:
        await player.show_hand()


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        await reaction.remove(user)


@client.event
async def on_raw_reaction_add(payload):
    member = payload.member

    if member.bot or (member not in players_dict):
        return

    player = players_dict[member]

    emoji = str(payload.emoji)

    # players_dict[member].receive_emoji(emoji)
    reaction_channel = client.get_channel(payload.channel_id)
    # reaction_guild = client.get_guild(payload.guild_id)
    if emoji == '🐢':
        await reaction_channel.send("TOORTOOLE")

    if emoji == "❌" and reaction_channel == player.channel:
        reaction_message = await reaction_channel.fetch_message(payload.message_id)
        await player.delete_message(reaction_message)

    if player == game.cur_active_player:
        if is_hand_event_active():
            card_type = transform_to_card_type(emoji)
            if card_type is not None:
                print(card_type)
                if card_type == FINISH_TURN:
                    await game.finish_turn()
                elif card_type in player.hand.cards:
                    card_idx = player.hand.cards.index(card_type)
                    await player.play_card(card_idx)
                await player.show_hand()
        else:
            choice = transform_to_int(emoji)
            if choice is not None:
                set_event(choice)


def kick_member(member):
    global game, players_dict
    game.kill(players_dict[member])


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel and not after.channel:
        kick_member(member)


@ client.command()
async def kick(ctx, member):
    kick_member(member)


@ client.command()
async def start(ctx):
    # startup functions
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        game_category = client.get_channel(GAME_CATEGORY)
        members = voice_channel.members
        game_channels = await create_voice_channels(members, game_category)

        players = [Player(member, channel)
                   for member, channel in game_channels.items()]

        global game
        global players_dict

        game = Game(players, len(players) - 1)
        players_dict = {member: player for member,
                        player in zip(members, players)}

        await do_turn(game)

with open("token.txt", "r") as token_file:
    token = token_file.readline()
    client.run(token)
