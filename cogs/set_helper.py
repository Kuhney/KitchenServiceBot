import discord
from discord import ApplicationContext
from discord.ext import commands

from embeds import SettingsEmbed
from save import Save


class SetHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=[937798823709929502], name="aushilfenstart",
                           description="Aushilfe wird diese Woche starten")
    async def set_helper(self, ctx: ApplicationContext):
        save = Save()
        save.week_idx = 0
        save.current_helper_id = save.helper_ids[0]
        print("bot answered to |set_helper| command issued by " + ctx.user.display_name)
        await ctx.respond(embed=SettingsEmbed(save).embed)
