from bot.utils import utils, db


async def kick_user(chat_id, user_id):
    if await utils.is_user_admin(chat_id, user_id):
        return False
    else:
        await utils.kick_user(chat_id, user_id)
        return True
