import logging.handlers

import kitchenservicebot.logger_config
from kitchenservicebot.bot import KitchenBot
from kitchenservicebot.save import Save
from kitchenservicebot.token_helper import get_token

logger = logging.getLogger("kitchenbot")

if __name__ == "__main__":
    kitchenservicebot.logger_config.setup_logging()

    logger.info("Starting kitchen bot")
    kitchen_bot = KitchenBot()
    kitchen_bot.setup()
    save = Save()

    kitchen_bot.run(get_token())
