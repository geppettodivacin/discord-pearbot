import discord

from discord.ext import commands

from . import pairing

def create_bot(connection, *args, **kwargs):
    bot = commands.Bot(*args, **kwargs)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}!')

    @bot.command()
    async def hello(ctx):
        await ctx.send(f'Hello from {bot.user}!')

    @bot.command()
    @commands.guild_only()
    async def register(ctx):
        with connection.transaction() as t:
            try:
                t.register_user(str(ctx.author.id), ctx.guild.id)
            except:
                await ctx.send(f'User {ctx.author.name} was already registered')
                return

            await ctx.send(f'User {ctx.author.name} registered')

    @bot.command()
    @commands.guild_only()
    async def users(ctx):
        with connection.transaction() as t:
            rows = t.users(ctx.guild.id)

            if not rows:
                await ctx.send('I have no users in my database!')
                return

            to_line = lambda row: f'<@{row[0]}>, {row[1]}'
            lines = map(to_line, rows)
            await ctx.send('\n'.join(lines))

    @bot.command()
    async def roles(ctx):
        members = ctx.message.mentions

        if not members:
            members = [ctx.author]

        member_roles = \
            [(member, map(lambda r: r.name, member.roles[1:]))
                for member in members]
        replies = \
            [f'Member {member.mention} has roles: {", ".join(roles)}'
                for (member, roles) in member_roles]

        for reply in replies:
            await ctx.send(reply)

    def is_admin(ctx):
        return any([role.permissions.administrator for role in ctx.author.roles])

    @bot.command()
    @commands.guild_only()
    @commands.check(is_admin)
    async def pair(ctx):
        with connection.transaction() as t:
            rows = t.unpaired_users(ctx.guild.id)

            if not rows:
                await ctx.send('I have no one left to pair!')
                return

            pairings = pairing.compute(list(rows))

            for pair in pairings.pairs:
                await ctx.send(f'Paired up <@{pair[0].id}> and <@{pair[1].id}>.')

            if pairings.leftovers:
                leftover_str = ', '.join([f'<@{user.id}>' for user in pairings.leftovers])
                await ctx.send(f'There were no pairings for these fine people: {leftover_str}')
            #TODO: Add the pairing to the database
    
    return bot
