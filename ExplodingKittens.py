import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


Client = discord.Client()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(
        f"Bot ready! Running version {str(discord.__version__)} Have fun exploding kittens!")


@client.command()
async def start(ctx):
    # startup functions
    voice_channel = ctx.author.voice.channel
    game_category = client.get_channel(863371910465191947)
    members = voice_channel.members
    game_channels = await create_voice_channels(members, game_category)


async def create_voice_channels(members, game_category):
    game_channels = []
    print(game_category)
    for member in members:
        for channel in game_category.channels:
            if channel.permissions_for(member).view_channel:
                game_channels.append(channel)
                break
        else:
            overwrites = {
                game_category.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            game_channels.append(await game_category.create_text_channel(member.display_name, overwrites=overwrites))
    return game_channels


# @client.event
# async def on_message(message):

#     # Bot doesn't reply to itself
#     if message.author.bot:
#         return

#     await message.channel.send("HI!")
#     await message.add_reaction('🐢')


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


client.run('ODYzMzU0Mjg3Mjc1MTE0NTA2.YOlrVg.Tq-izs2y5Vt3Bw0fEr5MgWdyMQo')
