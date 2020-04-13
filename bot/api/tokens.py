from bot import logger
from bot.utils import db


async def get_chat_id_by_token(token):
    chat = await db.get_chat_by_token(token, ["tg_id"])
    return chat["tg_id"]


async def verify_token(token):
    chat = await db.get_chat_by_token(token)
    return bool(chat)
