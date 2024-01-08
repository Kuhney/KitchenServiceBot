import discord
from discord import ApplicationContext
from discord.ext import commands

from embeds import SettingsEmbed
from save import Save


class Next(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=[937798823709929502], name="weiter", description="Spult eine Woche vor")
    async def kit_check(self, ctx: ApplicationContext):
        print("bot answered to |next| command issued by " + ctx.user.display_name)
        save = Save()
        save.skip_to_new_week()
        await ctx.respond("Zur nächsten Woche wurde gesprungen!", embed=SettingsEmbed(save).embed)
