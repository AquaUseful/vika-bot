from bot import BOT_ID
from bot.utils import utils


async def promote_user(chat_id, user_id):
    if await utils.is_user_admin(chat_id, user_id):
        return False
    else:
        await utils.promote_user(chat_id, user_id)
        return True


async def demote_user(chat_id, user_id):
    if user_id == BOT_ID:
        return False
    elif await utils.is_user_admin(chat_id, user_id):
        await utils.demote_user(chat_id, user_id)
        return True
    else:
        return False
