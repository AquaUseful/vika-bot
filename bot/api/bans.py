from bot.utils import utils, db


async def ban_user(chat_id, user_id):
    if not utils.is_user_admin(chat_id, user_id):
        await utils.ban_user(chat_id, user_id)
