import discord
from discord import ApplicationContext
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=[937798823709929502], name="help", description="Infos über den Küchendienst Bot")
    async def kit_help(self, ctx: ApplicationContext):
        embed = discord.Embed(title="Küchendienst Bot Commands", color=0xffffff)
        embed.add_field(name="`/help`", value="Ruft diese Nachricht auf", inline=False)
        embed.add_field(name="`/setup [@user, ...]`", value="Richtet den Küchendienst ein! Reihenfolge der "
                                                            "angegebenen Benutzer bestimmt "
                                                            "die Küchendienst Reihenfolge", inline=False)
        embed.add_field(name="`/start`", value="Startet den Bot wenn setup schonmal ausgeführt wurde", inline=False)
        embed.add_field(name="`/check`", value="Zeigt wer diese Woche mit Küchendienst an der Reihe ist", inline=False)
        embed.add_field(name="`/stop`", value="Stoppt die Küchendienst Benachrichtigung. "
                                              "Danach erneut kit setup/start", inline=False)
        embed.add_field(name="`/next`", value="Küchendienst wird an nächste Person gereicht")
        embed.add_field(name="`/time [day] [hour]`", value="Stelle ein wann Küchendienst wechseln soll\n [day] = "
                                                           "mo,di,mi,do,fr,sa,so \n [hour] = 0 - 23", inline=False)
        embed.add_field(name="`/hilfe [@user]`", value="Fügt den User als Aushilfe hinzu", inline=False)
        embed.add_field(name="`/helpme`", value="Küchendienst Aushilfe hilft sofort mit", inline=False)

        print("bot answered to |help| command issued by " + ctx.user.display_name)
        await ctx.respond(embed=embed)
