from bot import KitchenBot

from save import Save
from token_helper import get_token

kitchenBot = KitchenBot()
kitchenBot.setup()
save = Save()

kitchenBot.run(get_token())
