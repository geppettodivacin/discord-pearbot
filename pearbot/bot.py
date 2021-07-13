import discord

from discord.ext import commands

def create_bot(*args, **kwargs):
    bot = commands.Bot(*args, **kwargs)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}!')

    @bot.command()
    async def hello(ctx):
        await ctx.send(f'Hello from {bot.user}!')

    return bot
