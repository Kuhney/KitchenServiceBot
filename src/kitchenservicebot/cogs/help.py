import logging
from typing import TYPE_CHECKING

import discord
from discord import ApplicationContext
from discord.ext import commands

if TYPE_CHECKING:
    from kitchenservicebot.bot import KitchenBot

logger = logging.getLogger("kitchenbot.cogs")


class Help(commands.Cog):
    def __init__(self, bot: "KitchenBot") -> None:
        self.bot = bot

    @discord.slash_command(name="help", description="Infos über den Küchendienst Bot")
    async def kit_help(self, ctx: ApplicationContext) -> None:
        embed = discord.Embed(title="Küchendienst Bot Commands")
        embed.add_field(name="`/help`", value="Ruft diese Nachricht auf", inline=False)
        embed.add_field(name="`/setup`", value="Richtet den Küchendienst ein!", inline=False)
        embed.add_field(name="`/check`", value="Zeigt die Küchendienst Informationen an", inline=False)
        embed.add_field(name="`/weiter`", value="Spult eine Woche vor", inline=False)
        embed.add_field(name="`/aushilfestart`", value="Startet die Aushilfe diese Woche", inline=False)

        logger.info("bot answered to |help| command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=embed)
