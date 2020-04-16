from bot.utils import db


async def get_chat_members(chat_id):
    chat = await db.get_chat(chat_id, ["members"])
    users = chat["members"]
    return users


async def get_chat_info(chat_id):
    chat = await db.get_chat(chat_id, {"_id": False})
    return chat
