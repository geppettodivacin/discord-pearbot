import discord

class Client(discord.Client):
    async def on_ready(self):
        print (f'Logged in as {self.user}!')
