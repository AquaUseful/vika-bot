import telethon
from bot.utils import utils, db


async def ban_user(chat_id, user_id):
    if await utils.is_user_admin(chat_id, user_id):
        return False
    else:
        try:
            await utils.ban_user(chat_id, user_id)
            return True
        except telethon.errors.ChatAdminRequiredError:
            return False


async def unban_user(chat_id, user_id):
    if await utils.is_user_banned(chat_id, user_id):
        try:
            await utils.unban_user(chat_id, user_id)
            return True
        except telethon.errors.ChatAdminRequiredError:
            return False
    else:
        return False
