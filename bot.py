import discord

from cogs.check import Check
from cogs.help import Help
from cogs.next import Next
from cogs.setup import Setup


class KitchenBot(discord.Bot):
    async def on_ready(self):
        print('Bot has logged in as {0.user}'.format(self))

    def setup(self):
        self.add_cog(Help(self))
        self.add_cog(Setup(self))
        self.add_cog(Check(self))
        self.add_cog(Next(self))
