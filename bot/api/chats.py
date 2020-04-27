from bot.utils import db, utils


async def get_chat_member_ids(chat_id):
    chat = await db.get_chat(chat_id, ["members"])
    users = chat["members"]
    return users


async def get_chat_info(chat_id):
    chat = await db.get_chat(chat_id, {"_id": False, "token": False, "welcome": False})
    return chat


async def get_chat_members(chat_id):
    members = await utils.get_members(chat_id)
    return members
