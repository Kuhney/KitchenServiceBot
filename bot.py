import discord

from Scheduler import WeeklyScheduler
from cogs.check import Check
from cogs.help import Help
from cogs.next import Next
from cogs.set_helper import SetHelper
from cogs.setup import Setup
from embeds import SettingsEmbed
from save import Save


class KitchenBot(discord.Bot):
    def __init__(self):
        super().__init__()
        self.save = Save()
        self.scheduler = WeeklyScheduler(self.change_week, self.save)

    async def on_ready(self):
        print('Bot has logged in as {0.user}'.format(self))
        self.scheduler.start_schedule()

    def setup(self):
        self.add_cog(Help(self))
        self.add_cog(Setup(self))
        self.add_cog(Check(self))
        self.add_cog(Next(self))
        self.add_cog(SetHelper(self))

    async def change_week(self):
        self.save.skip_to_new_week()
        await self.get_channel(self.save.channel).send("Der Küchendienst hat sich aktualisiert",
                                                       embed=SettingsEmbed(self.save).embed)
