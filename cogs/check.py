import discord
from discord import ApplicationContext
from discord.ext import commands

from embeds import SettingsEmbed
from save import Save


class Check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=[937798823709929502], name="check", description="Küchendienst Status")
    async def kit_check(self, ctx: ApplicationContext):
        print("bot answered to |check| command issued by " + ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(Save()).embed)
