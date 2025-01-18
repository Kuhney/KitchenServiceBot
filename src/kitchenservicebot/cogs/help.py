"""Help Cog."""

import logging

import discord
from discord import ApplicationContext
from discord.ext import commands

logger = logging.getLogger("kitchenbot.cogs")


class Help(commands.Cog):
    """Help Cog."""

    @discord.slash_command(name="kommandos", description="Kommandos zum Steuern des Küchendienst Bots")
    async def kit_help(self, ctx: ApplicationContext) -> None:
        """Command to show a help message with commandos.

        Args:
            ctx (ApplicationContext): The context of the command

        """
        embed = discord.Embed(title="Küchendienst Bot Commands")
        embed.add_field(name="`/help`", value="Ruft diese Nachricht auf", inline=False)
        embed.add_field(name="`/setup`", value="Richtet den Küchendienst ein!", inline=False)
        embed.add_field(name="`/check`", value="Zeigt die Küchendienst Informationen an", inline=False)
        embed.add_field(name="`/weiter`", value="Spult eine Woche vor", inline=False)
        embed.add_field(name="`/aushilfestart`", value="Startet die Aushilfe diese Woche", inline=False)

        logger.info("bot answered to </kommandos> command issued by %s", ctx.user.display_name)
        await ctx.respond(embed=embed)
