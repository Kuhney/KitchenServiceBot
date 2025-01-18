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


class Next(commands.Cog):
    def __init__(self, bot: "KitchenBot") -> None:
        self.bot = bot

    @discord.slash_command(name="weiter", description="Spult eine Woche vor")
    async def kit_check(self, ctx: ApplicationContext) -> None:
        logger.info("bot answered to |next| command issued by %s", ctx.user.display_name)
        save = Save()
        save.skip_to_new_week()
        await ctx.respond("Zur nächsten Woche wurde gesprungen!", embed=SettingsEmbed(save).embed)
