"""Main module for the kitchen service bot."""

import logging.handlers

import kitchenservicebot.logger_config
from kitchenservicebot.bot import KitchenBot
from kitchenservicebot.token_helper import get_token

logger = logging.getLogger("kitchenbot")


def main() -> None:
    """Start the kitchen bot."""
    kitchenservicebot.logger_config.setup_logging()

    logger.info("Starting kitchen bot")
    kitchen_bot = KitchenBot()
    kitchen_bot.setup()

    kitchen_bot.run(get_token())


if __name__ == "__main__":
    main()
