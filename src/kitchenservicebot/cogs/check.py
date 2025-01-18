import logging
from typing import TYPE_CHECKING

import discord
from discord import ApplicationContext
from discord.ext import commands

from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.save import Save

if TYPE_CHECKING:
    from kitchenservicebot.bot import KitchenBot

logger = logging.getLogger("kitchenbot.cogs")


class Check(commands.Cog):
    def __init__(self, bot: "KitchenBot") -> None:
        self.bot = bot

    @discord.slash_command(name="check", description="Küchendienst Status")
    async def kit_check(self, ctx: ApplicationContext) -> None:
        logger.info("bot answered to |check| command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(Save()).embed)
