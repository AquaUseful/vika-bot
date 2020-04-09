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
    old_user = await mongodb.users.find_one({"tg_id": user.id})
    if old_user:
        await mongodb.users.replace_one({"_id": old_user["_id"]}, new_user)
    else:
        await mongodb.users.insert_one(new_user)
    logger.debug("User %s added", user.id)


async def add_chat_to_db(chat: telethon.types.Chat):
    admins = await utils.get_admins(chat.id, only_ids=True)
    members = await utils.get_members(chat.id, only_ids=True)
    new_chat = {
        "tg_id": chat.id,
        "title": chat.title,
        "members": members,
        "admins": admins,
        "welcome": None
    }
    old_chat = await mongodb.chats.find_one({"tg_id": chat.id})
    if old_chat:
        await mongodb.chats.replace_one({"_id": old_chat["_id"]}, new_chat)
    else:
        await mongodb.chats.insert_one(new_chat)
    logger.debug("Chat %s added", chat.id)


async def add_note_to_db(chat_id: int, title: str, text: str):
    new_note = {
        "chat_id": chat_id,
        "title": title,
        "text": text
    }
    old_note = await mongodb.notes.find_one({"chat_id": chat_id, "title": title})
    if old_note:
        await mongodb.notes.replace_one({"id:": old_note["_id"]}, new_note)
    else:
        await mongodb.notes.insert_one(new_note)
    logger.debug("Note %s added to chat %s", title, chat_id)


async def get_note_by_id(doc_id, projection=None):
    note = await mongodb.notes.find_one({"_id": doc_id}, projection)
    return note


async def get_note(chat_id: int, title: str, projection=None):
    note = await mongodb.notes.find_one(
        {"chat_id": chat_id, "title": title}, projection)
    return note


async def delete_note(chat_id: int, title: str):
    res = await mongodb.notes.delete_one({"chat_id": chat_id, "title": title})
    return res.deleted_count > 0


async def get_chat(tg_id: int, projection=None):
    chat = await mongodb.chats.find_one({"tg_id": tg_id}, projection)
    return chat


async def update_chat(tg_id: int, query):
    await mongodb.chats.update_one({"tg_id": tg_id}, query)


async def change_chat_id(old_id: int, new_id: int):
    await mongodb.chats.update_one({"tg_id": old_id}, {"$set": {"tg_id": new_id}})
    await mongodb.notes.update_many({"chat_id": old_id},
                                    {"$set": {"chat_id": new_id}})
    logger.debug("Changed chat's id from %s to %s", old_id, new_id)
