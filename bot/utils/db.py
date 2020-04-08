import telethon
import asyncio
import pymongo
from bot import bot, mongodb, logger
from bot.utils import utils


async def add_user_to_db(user: telethon.types.User):
    new_user = {
        "tg_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "is_bot": user.username
    }
    old_user = mongodb.users.find_one({"tg_id": user.id})
    if old_user:
        res = mongodb.users.replace_one({"_id": old_user["_id"]}, new_user)
    else:
        res = mongodb.users.insert_one(new_user)
    logger.debug(res)


async def add_chat_to_db(chat: telethon.types.Chat):
    admins = await utils.get_admins(chat.id, only_ids=True)
    members = await utils.get_members(chat.id, only_ids=True)
    new_chat = {
        "tg_id": chat.id,
        "title": chat.title,
        "members": members,
        "admins": admins,
        "warnlimit": 5,
        "disabled": []
    }
    old_chat = mongodb.chats.find_one({"tg_id": chat.id})
    if old_chat:
        res = mongodb.chats.replace_one({"_id": old_chat["_id"]}, new_chat)
    else:
        res = mongodb.chats.insert_one(new_chat)
    logger.debug(res)


async def add_note_to_db(chat_id: int, title: str, text: str):
    new_note = {
        "chat_id": chat_id,
        "title": title,
        "text": text
    }
    old_note = mongodb.notes.find_one({"chat_id": chat_id, "title": title})
    if old_note:
        res = mongodb.notes.replace_one({"id:": old_note["_id"]}, new_note)
    else:
        res = mongodb.notes.insert_one(new_note)
    logger.debug(res)


async def get_note_text(chat_id: int, title: str):
    note = mongodb.notes.find_one({"chat_id": chat_id, "title": title},
                                  ["text"])
    if note:
        return note["text"]


async def delete_note(chat_id: int, title: str):
    res = mongodb.notes.delete_one({"chat_id": chat_id, "title": title})
    return res.deleted_count > 0


async def get_chat(chat_id: int, projection=None):
    chat = mongodb.chats.find_one({"chat_id": chat_id}, projection)
    return chat
