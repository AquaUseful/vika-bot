from bot.utils import utils, db


async def ban_user(chat_id, user_id):
    if await utils.is_user_admin(chat_id, user_id):
        return False
    else:
        await utils.ban_user(chat_id, user_id)
        return True


async def unban_user(chat_id, user_id):
    if await utils.is_user_banned(chat_id, user_id):
        await utils.unban_user(chat_id, user_id)
        return True
    else:
        return False
