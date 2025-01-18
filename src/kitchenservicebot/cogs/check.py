import discord
from discord import ApplicationContext
from discord.ext import commands

from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.save import Save


class Check(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.slash_command(name="check", description="Küchendienst Status")
    async def kit_check(self, ctx: ApplicationContext) -> None:
        print("bot answered to |check| command issued by " + ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(Save()).embed)
