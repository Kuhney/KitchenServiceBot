"""Status Cog."""

import logging

import discord
from discord import ApplicationContext
from discord.ext import commands

from kitchenservicebot.bot_config import BotConfiguration
from kitchenservicebot.embeds import SettingsEmbed

logger = logging.getLogger("kitchenbot.cogs")


class Status(commands.Cog):
    """Check Cog."""

    @discord.slash_command(name="status", description="Küchendienst Status")
    async def kit_status(self, ctx: ApplicationContext) -> None:
        """Command to check the current status of the kitchen service.

        Args:
            ctx (ApplicationContext): The context of the command

        """
        logger.info("bot answered to </status> command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(BotConfiguration()).embed)
