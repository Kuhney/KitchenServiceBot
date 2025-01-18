import logging

import discord

from kitchenservicebot.cogs.check import Check
from kitchenservicebot.cogs.help import Help
from kitchenservicebot.cogs.next import Next
from kitchenservicebot.cogs.set_helper import SetHelper
from kitchenservicebot.cogs.setup import Setup
from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.save import Save
from kitchenservicebot.scheduler import WeeklyScheduler

logger = logging.getLogger(__name__)


class KitchenBot(discord.Bot):
    def __init__(self) -> None:
        super().__init__()
        self.save = Save()
        self.scheduler = WeeklyScheduler(self.change_week, self.save)

    async def on_ready(self) -> None:
        logger.info("Bot has logged in as %s", self.user)
        self.scheduler.start_schedule()

    def setup(self) -> None:
        self.add_cog(Help(self))
        self.add_cog(Setup(self))
        self.add_cog(Check(self))
        self.add_cog(Next(self))
        self.add_cog(SetHelper(self))
        logger.info("Bot added all cogs")

    async def change_week(self) -> None:
        self.save.skip_to_new_week()
        await self.get_channel(self.save.channel).send(
            "Der Küchendienst hat sich aktualisiert",
            embed=SettingsEmbed(self.save).embed,
        )
