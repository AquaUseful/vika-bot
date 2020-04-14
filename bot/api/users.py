import telethon
from bot import bot
from bot.utils import db


async def get_users_info(user_ids):
    users = await bot.get_entity(user_ids)
    return users
