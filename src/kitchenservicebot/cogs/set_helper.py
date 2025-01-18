"""SetHelper Cog."""

import logging

import discord
from discord import ApplicationContext
from discord.ext import commands

from kitchenservicebot.bot_config import BotConfiguration
from kitchenservicebot.embeds import SettingsEmbed

logger = logging.getLogger("kitchenbot.cogs")


class SetHelper(commands.Cog):
    """SetHelper Cog."""

    @discord.slash_command(name="brauche_hilfe", description="Aushilfe wird diese Woche starten")
    async def set_helper(self, ctx: ApplicationContext) -> None:
        """Command to set the helper for the current week.

        Args:
            ctx (ApplicationContext): The context of the command

        """
        save = BotConfiguration()
        save.week_idx = 0
        save.current_helper_id = save.helper_ids[0]
        logger.info("bot answered to </brauche hilfe> command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(save).embed)
