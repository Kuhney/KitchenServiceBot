"""Module containing the BotConfiguration class."""

import json
import logging
from pathlib import Path

from kitchenservicebot.enums import Weekday

logger = logging.getLogger(__name__)


class BotConfiguration:
    """Class to store the configuration of the bot."""

    def __init__(self) -> None:
        """Initialize the BotConfiguration."""
        self.worker_ids: list[int] = []
        self.current_worker_id: int | None = None
        self.helper_ids: list[int] = []
        self.current_helper_id: int | None = None
        self.change_time_day: Weekday = Weekday.MONDAY
        self.change_time_time: int = 0
        self.week_idx: int = 0
        self.channel: int | None = None
        self.load_save_file()

    def load_save_file(self) -> None:
        """Load the configuration from the savefile."""
        try:
            with Path("savefile.json").open() as config_file:
                conf_dict = json.load(config_file)
                self.worker_ids = conf_dict["workers"]
                self.current_worker_id = conf_dict["current_worker"]
                self.helper_ids = conf_dict["helper"]
                self.change_time_day = Weekday(value=conf_dict["day"])
                self.change_time_time = conf_dict["time"]
                self.week_idx = conf_dict["week_idx"]
                self.channel = conf_dict["channel"]
        except FileNotFoundError:
            logger.info("No savefile found. Created one")
            self.save_to_file()

    def save_to_file(self) -> None:
        """Save the configuration to the savefile."""
        with Path("savefile.json").open("w") as config_file:
            json.dump(
                {
                    "workers": self.worker_ids,
                    "current_worker": self.current_worker_id,
                    "helper": self.helper_ids,
                    "day": self.change_time_day.value,
                    "time": self.change_time_time,
                    "week_idx": self.week_idx,
                    "channel": self.channel,
                },
                config_file,
                indent=4,
            )
            config_file.close()
        logger.info("Saved configuration to %s", config_file.name)

    def get_user_by_id(self, idx: int) -> str:
        """Get the user by the given id."""
        return "<@" + str(idx) + ">"

    def advance_to_next_week(self) -> None:
        """Advance to the next week and save the configuration."""
        self.week_idx += 1

        self.current_worker_id = self.worker_ids[0]
        self.worker_ids.append(self.worker_ids[0])
        self.worker_ids.pop(0)

        if self.week_idx % (len(self.worker_ids) + 1) == 0:
            self.current_helper_id = self.helper_ids[0]
        elif self.current_helper_id is not None:
            self.current_helper_id = None
        self.save_to_file()
