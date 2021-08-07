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
            try:
                t.register_user(ctx.author.name, ctx.guild.id)
            except:
                await ctx.send(f'User {ctx.author.name} was already registered')
                return

            await ctx.send(f'User {ctx.author.name} registered')

    @bot.command()
    async def users(ctx):
        with connection.transaction() as t:
            cursor = t.users(ctx.guild.id)
            rows = cursor.fetchall()

            if not rows:
                await ctx.send('I have no users in my database!')
                return

            to_line = lambda row: ', '.join([str(col) for col in row])
            lines = map(to_line, rows)
            await ctx.send('\n'.join(lines))

    return bot
