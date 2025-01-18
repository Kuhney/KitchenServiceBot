import discord

from kitchenservicebot.cogs.check import Check
from kitchenservicebot.cogs.help import Help
from kitchenservicebot.cogs.next import Next
from kitchenservicebot.cogs.set_helper import SetHelper
from kitchenservicebot.cogs.setup import Setup
from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.save import Save
from kitchenservicebot.Scheduler import WeeklyScheduler


class KitchenBot(discord.Bot):
    def __init__(self) -> None:
        super().__init__()
        self.save = Save()
        self.scheduler = WeeklyScheduler(self.change_week, self.save)

    async def on_ready(self) -> None:
        print(f"Bot has logged in as {self.user}")
        self.scheduler.start_schedule()

    def setup(self) -> None:
        self.add_cog(Help(self))
        self.add_cog(Setup(self))
        self.add_cog(Check(self))
        self.add_cog(Next(self))
        self.add_cog(SetHelper(self))

    async def change_week(self) -> None:
        self.save.skip_to_new_week()
        await self.get_channel(self.save.channel).send(
            "Der Küchendienst hat sich aktualisiert",
            embed=SettingsEmbed(self.save).embed,
        )
