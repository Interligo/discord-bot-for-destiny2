import os
import discord
from discord.ext import commands

from load_environment import load_environment


# TODO: add logger

load_environment()

BOT_CLIENT_ID = os.getenv('BOT_CLIENT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(pass_context=True)
async def commands(ctx):
    message_author = ctx.message.author

    await ctx.send(f'{message_author.mention}, скоро здесь будет список команд.')


bot.run(BOT_TOKEN)
