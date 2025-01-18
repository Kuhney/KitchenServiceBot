"""Next Cog."""

import logging

import discord
from discord import ApplicationContext
from discord.ext import commands

from kitchenservicebot.bot_config import BotConfiguration
from kitchenservicebot.embeds import SettingsEmbed

logger = logging.getLogger("kitchenbot.cogs")


class Next(commands.Cog):
    """Next Cog."""

    @discord.slash_command(name="weiter", description="Spult eine Woche vor")
    async def kit_next(self, ctx: ApplicationContext) -> None:
        """Command to advance to the next week.

        Args:
            ctx (ApplicationContext): The context of the command

        """
        logger.info("bot answered to </weiter> command issued by %s", ctx.user.display_name)
        save = BotConfiguration()
        save.advance_to_next_week()
        await ctx.respond("Zur nächsten Woche wurde gesprungen!", embed=SettingsEmbed(save).embed)
