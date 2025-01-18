"""Embeds for the bot."""

import logging

import discord

from kitchenservicebot.bot_config import BotConfiguration

logger = logging.getLogger(__name__)


class SettingsEmbed:
    """Embed for the settings of the bot."""

    def __init__(self, config: BotConfiguration) -> None:
        """Initialize the SettingsEmbed with the given configuration.

        Args:
            config (BotConfiguration): Bot configuration which will be used.

        """
        self.config = config
        workers: str = str([self.config.get_user_by_id(x) for x in self.config.worker_ids])
        helpers: str = str([self.config.get_user_by_id(x) for x in self.config.helper_ids])
        if self.config.current_worker_id is None:
            logger.error("No current worker set")
            return
        active_worker: str = self.config.get_user_by_id(self.config.current_worker_id)

        if self.config.current_helper_id:
            active_worker += " unterstützt von " + self.config.get_user_by_id(self.config.current_helper_id)

        self.embed = discord.Embed(title="Küchendienst Einstellungen")

        self.embed.add_field(name="Küchendienst der Woche", value=active_worker, inline=False)
        self.embed.add_field(name="Anstehender Küchendienst", value=workers, inline=False)
        self.embed.add_field(name="Mögliche Aushilfe", value=helpers, inline=False)
        self.embed.add_field(
            name="Wechsel am",
            value=self.config.change_time_day.display_name + " um " + str(self.config.change_time_time) + " Uhr",
            inline=False,
        )
