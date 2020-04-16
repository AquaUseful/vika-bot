import telethon
from bot import bot
from bot.utils import db


async def get_users_info(user_ids):
    users = await bot.get_entity(user_ids)
    return users


async def get_last_photo(user_id, big=False):
    user = await get_users_info(user_id)
    photo = await bot.download_profile_photo(user, file=bytes, download_big=big)
    return photo
