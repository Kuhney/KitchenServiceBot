"""Scheduler module."""

import logging
from collections.abc import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from kitchenservicebot.bot_config import BotConfiguration

logger = logging.getLogger(__name__)


class WeeklyScheduler:
    """WeeklyScheduler class."""

    def __init__(self, job_func: Callable, config: BotConfiguration) -> None:
        """Initialize the WeeklyScheduler.

        Args:
            job_func (Callable): function to be called when scheduled
            config (BotConfiguration): configuration of the bot

        """
        self.config = config
        self.job_func = job_func
        self.scheduler = AsyncIOScheduler()
        self.update_jobs()

    def start_schedule(self) -> None:
        """Start the scheduler."""
        self.scheduler.start()

    def update_jobs(self) -> None:
        """Update the jobs in the scheduler."""
        self.config.load_save_file()
        self.scheduler.remove_all_jobs()
        self.scheduler.add_job(
            self.job_func,
            "cron",
            day_of_week=self.config.change_time_day.cron,
            hour=self.config.change_time_time,
        )
        logger.info("Updated Job Schedule")
