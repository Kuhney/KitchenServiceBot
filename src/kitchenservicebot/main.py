from kitchenservicebot.bot import KitchenBot
from kitchenservicebot.save import Save
from kitchenservicebot.token_helper import get_token

kitchen_bot = KitchenBot()
kitchen_bot.setup()
save = Save()

kitchen_bot.run(get_token())
