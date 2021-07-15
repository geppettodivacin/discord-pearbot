import discord

from discord.ext import commands

def create_bot(connection, *args, **kwargs):
    bot = commands.Bot(*args, **kwargs)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}!')

    @bot.command()
    async def hello(ctx):
        await ctx.send(f'Hello from {bot.user}!')

    @bot.command()
    async def register(ctx):
        with connection.transaction() as t:
            t.register_user(ctx.author.name, ctx.guild.id)
            await ctx.send(f'User {ctx.author.name} registered')

    @bot.command()
    async def users(ctx):
        with connection.transaction() as t:
            cursor = t.users ()
            to_line = lambda row: ', '.join([str(col) for col in row])
            lines = map(to_line, cursor)
            await ctx.send('\n'.join(lines))

    return bot
