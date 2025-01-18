"""Module containing the Setup Cog."""

import logging
from typing import TYPE_CHECKING, cast

import discord
from discord import ApplicationContext, ComponentType, Interaction, Member, SelectOption, User, ui
from discord.ext import commands

from kitchenservicebot.bot_config import BotConfiguration
from kitchenservicebot.embeds import SettingsEmbed
from kitchenservicebot.enums import Weekday
from kitchenservicebot.scheduler import WeeklyScheduler

if TYPE_CHECKING:
    from kitchenservicebot.bot import KitchenBot

logger = logging.getLogger("kitchenbot.cogs")


class Setup(commands.Cog):
    """Setup Cog."""

    def __init__(self, bot: "KitchenBot") -> None:
        """Initialize the Setup Cog.

        Args:
            bot (KitchenBot): The bot instance

        """
        self.bot = bot
        self.save = BotConfiguration()

    @discord.slash_command(name="konfigurieren", description="Stelle den Küchendienst ein")
    async def setup(self, ctx: ApplicationContext) -> None:
        """Command to setup the kitchen service.

        Args:
            ctx (ApplicationContext): The context of the command

        """
        self.save.channel = ctx.channel_id
        logger.info("bot answered to </konfigurieren> command issued by %s", ctx.user.display_name)
        await ctx.respond(
            "Wähle Helfer in der gewünschten Reihenfolge!",
            view=SelectWorkerView(self.save, self.bot.scheduler),
        )


class TimeInputModal(discord.ui.Modal):
    """Modal to input the time."""

    def __init__(self, config: BotConfiguration, scheduler: WeeklyScheduler, title: str) -> None:
        """Initialize the TimeInputModal.

        Args:
            config (BotConfiguration): configuration of the bot
            scheduler (WeeklyScheduler): handle of the scheduler
            title (str): title of the modal

        """
        super().__init__(title=title)
        self.save = config
        self.scheduler = scheduler
        self.add_item(discord.ui.InputText(label="Uhrzeit zum Wechseln des Küchendienstes (0-24)"))

    async def callback(self, interaction: discord.Interaction) -> None:
        """Call when the time modal is submitted."""
        entered_time = self.children[0].value
        if entered_time is None:
            await interaction.response.send_message("Bitte gebe eine Stunde ein!")
            return

        if 0 <= int(entered_time) <= 24:  # noqa: PLR2004
            self.save.change_time_time = int(entered_time)
            self.save.save_to_file()
            self.scheduler.update_jobs()
            await interaction.response.send_message(
                "Einstellung erfolgreich durchgeführt!",
                embeds=[SettingsEmbed(self.save).embed],
            )
        else:
            await interaction.response.send_message("Falsches Uhrzeitformat! Führe das Setup erneut durch!")


class SelectDayView(ui.View):
    """View to select the day of the week."""

    def __init__(self, config: BotConfiguration, scheduler: WeeklyScheduler) -> None:
        """Initialize the SelectDayView.

        Args:
            config (BotConfiguration): Configuration of the bot
            scheduler (WeeklyScheduler): Handle of the scheduler

        """
        super().__init__()
        self.save = config
        self.scheduler = scheduler

    @discord.ui.select(
        select_type=ComponentType.string_select,
        options=[SelectOption(label=weekday.display_name, value=str(weekday.value)) for weekday in Weekday],
    )
    async def select_callback(self, select: ui.Select, interaction: Interaction) -> None:
        """Call when the day is selected."""
        selected = cast(str, select.values[0])  # select_type=ComponentType.string_select,
        self.save.change_time_day = Weekday(value=int(selected))
        modal = TimeInputModal(self.save, self.scheduler, title="Gebe die Uhrzeit ein")
        await interaction.response.send_modal(modal)


class SelectHelperView(ui.View):
    """View to select the helper."""

    def __init__(self, config: BotConfiguration, scheduler: WeeklyScheduler) -> None:
        """Initialize the SelectHelperView.

        Args:
            config (BotConfiguration): Configuration of the bot
            scheduler (WeeklyScheduler): Handle of the scheduler

        """
        super().__init__()
        self.save = config
        self.scheduler = scheduler

    @discord.ui.select(
        select_type=ComponentType.user_select,
        min_values=1,
        max_values=10,
    )
    async def select_callback(self, select: ui.Select, interaction: Interaction) -> None:
        """Call when the helper is selected."""
        selected = cast(list[Member | User], select.values)
        self.save.helper_ids = [user.id for user in selected]
        self.save.current_helper_id = selected[0].id
        await interaction.response.send_message(
            "Wähle an welchem Tag der Küchendienst gewechselt werden soll!",
            view=SelectDayView(self.save, self.scheduler),
        )


class SelectWorkerView(discord.ui.View):
    """View to select the worker."""

    def __init__(self, config: BotConfiguration, scheduler: WeeklyScheduler) -> None:
        """Initialize the SelectWorkerView.

        Args:
            config (BotConfiguration): Configuration of the bot
            scheduler (WeeklyScheduler): Handle of the scheduler

        """
        super().__init__()
        self.save = config
        self.scheduler = scheduler

    @discord.ui.select(
        select_type=discord.ComponentType.user_select,
        min_values=2,
        max_values=10,
    )
    async def select_callback(self, select: ui.Select, interaction: Interaction) -> None:
        """Call when the worker is selected.

        Args:
            select (ui.Select): handle of the selected option
            interaction (Interaction): handle of the interaction

        """
        selected = cast(list[Member | User], select.values)
        self.save.worker_ids = [x.id for x in selected]
        self.save.current_worker_id = selected[0].id
        await interaction.response.send_message(
            "Wähle die Aushilfe aus!",
            view=SelectHelperView(self.save, self.scheduler),
        )
