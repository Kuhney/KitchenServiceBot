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


class SetHelper(commands.Cog):
    def __init__(self, bot: "KitchenBot") -> None:
        self.bot = bot

    @discord.slash_command(name="aushilfenstart", description="Aushilfe wird diese Woche starten")
    async def set_helper(self, ctx: ApplicationContext) -> None:
        save = Save()
        save.week_idx = 0
        save.current_helper_id = save.helper_ids[0]
        logger.info("bot answered to |set_helper| command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(save).embed)
