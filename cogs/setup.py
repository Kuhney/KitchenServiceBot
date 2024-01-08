import discord
from discord import ApplicationContext, Interaction, SelectOption
from discord.ext import commands

from embeds import SettingsEmbed
from enums import Weekday
from save import Save


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.save = Save()

    @discord.slash_command(guild_ids=[937798823709929502], name="setup", description="Stelle den Küchendienst ein")
    async def flavor(self, ctx: ApplicationContext):
        print("bot answered to |setup| command issued by " + ctx.user.display_name)
        await ctx.respond("Wähle Helfer in der gewünschten Reihenfolge!", view=SelectWorkerView(self.save))


class TimeInputModal(discord.ui.Modal):
    def __init__(self, save: Save, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.save = save
        self.add_item(discord.ui.InputText(label="Uhrzeit"))

    async def callback(self, interaction: discord.Interaction):
        inputted_time: int = int(self.children[0].value)
        if 0 <= inputted_time <= 24:
            self.save.change_time_time = inputted_time
            self.save.save_to_file()
            await interaction.response.send_message(embeds=[SettingsEmbed(self.save).embed])
        else:
            self.stop()
            modal = TimeInputModal(self.save,
                                   title="Gebe die Uhrzeit ein")
            await interaction.response.send_message("Falsches Uhrzeitformat! Führe das Setup erneut durch!")


class SelectDayView(discord.ui.View):
    def __init__(self, save: Save):
        super().__init__()
        self.save = save

    @discord.ui.select(
        select_type=discord.ComponentType.select,
        options=[SelectOption(
            label=weekday.display_name,
            value=str(weekday.value)
        ) for weekday in Weekday]
    )
    async def select_callback(self, select, interaction: Interaction):
        self.save.change_time_day = Weekday(value=int(select.values[0]))
        modal = TimeInputModal(self.save,
                               title="Gebe die Uhrzeit ein")
        await interaction.response.send_modal(modal)


class SelectWorkerView(discord.ui.View):
    def __init__(self, save: Save):
        super().__init__()
        self.save = save

    @discord.ui.select(
        select_type=discord.ComponentType.user_select,
        min_values=2,
        max_values=10,
    )
    async def select_callback(self, select, interaction: Interaction):
        self.save.worker_ids = list(map(lambda x: x.id, select.values))
        self.save.current_worker_id = select.values[0].id
        await interaction.response.send_message("Wähle die Aushilfe aus!", view=SelectHelperView(self.save))


class SelectHelperView(discord.ui.View):
    def __init__(self, save: Save):
        super().__init__()
        self.save = save

    @discord.ui.select(
        select_type=discord.ComponentType.user_select,
        min_values=1,
        max_values=10,
    )
    async def select_callback(self, select, interaction: Interaction):
        self.save.helper_ids = list(map(lambda x: x.id, select.values))
        self.save.current_helper_id = select.values[0].id
        await interaction.response.send_message("Wähle an welchem Tag der Küchendienst gewechselt werden soll!",
                                                view=SelectDayView(self.save))
