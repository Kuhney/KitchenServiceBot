"""Bot class for the kitchen service bot."""

import logging
from typing import cast

import discord

from kitchenservicebot.bot_config import BotConfiguration
from kitchenservicebot.cogs.help import Help
from kitchenservicebot.cogs.next import Next
from kitchenservicebot.cogs.set_helper import SetHelper
from kitchenservicebot.cogs.setup import Setup
from kitchenservicebot.cogs.status import Status
from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.scheduler import WeeklyScheduler

logger = logging.getLogger(__name__)


class KitchenBot(discord.Bot):
    """KitchenBot class."""

    def __init__(self) -> None:
        """Initialize the KitchenBot."""
        super().__init__()
        self.config = BotConfiguration()
        self.scheduler = WeeklyScheduler(job_func=self.on_next_week, config=self.config)

    async def on_ready(self) -> None:
        """Handle the on_ready event of the bot."""
        logger.info("Bot has logged in as %s", self.user)
        self.scheduler.start_schedule()

    def setup(self) -> None:
        """Add all cogs to the bot."""
        self.add_cog(Help(self))
        self.add_cog(Setup(self))
        self.add_cog(Status(self))
        self.add_cog(Next(self))
        self.add_cog(SetHelper(self))
        logger.info("Bot added all cogs")

    async def on_next_week(self) -> None:
        """Handle the beginning of a new week.

        Send a message to the, on setup configured, channel that a week has passed
        and the kitchen service has been updated.
        """
        self.config.advance_to_next_week()
        if self.config.channel is None:
            logger.error("Could not send message: Channel is not set")
        else:
            channel = self.get_channel(self.config.channel)
            if channel is None:
                logger.error("Could not send message: Channel not found")
                return
            channel = cast(discord.TextChannel, channel)
            await channel.send(
                "Der Küchendienst hat sich aktualisiert!",
                embed=SettingsEmbed(self.config).embed,
            )
