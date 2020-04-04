import telethon
import asyncio
from bot import bot, mongodb, logger
from bot.utils import utils


async def add_user_to_db(user: telethon.types.User):
    new_user = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "is_bot": user.username
    }
    old_user = mongodb.users.find_one({"user_id": user.id})
    if old_user:
        res = mongodb.users.replace_one({"_id": old_user["_id"]}, new_user)
    else:
        res = mongodb.users.insert_one(new_user)
    logger.debug(res)


async def add_chat_to_db(chat: telethon.types.Chat):
    admins = await utils.get_admins(chat.id, only_ids=True)
    members = await utils.get_admins(chat.id, only_ids=True)
    new_chat = {
        "chat_id": chat.id,
        "title": chat.title,
        "members": members,
        "admins": admins,
        "warnlimit": 5,
        "disabled": []
    }
    old_chat = mongodb.chats.find_one({"chat_id": chat.id})
    if old_chat:
        res = mongodb.chats.replace_one({"_id": old_chat["_id"]}, new_chat)
    else:
        res = mongodb.chats.insert_one(new_chat)
    logger.debug(res)
