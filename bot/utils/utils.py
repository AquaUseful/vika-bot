import telethon
import importlib
import sys
import asyncio
import re
from bot import ADMINS, bot, logger
from bot.modules import ALL_MODULES
from bot.utils import db
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsBanned


async def get_banned(chat_id: int, only_ids=False):
    banned = await bot.get_participants(chat_id, filter=ChannelParticipantsBanned(""))
    if only_ids:
        banned = tuple(map(lambda member: member.id, banned))
    return banned


async def get_admins(chat_id: int, only_ids=False):
    admins = await bot.get_participants(chat_id, filter=ChannelParticipantsAdmins())
    if only_ids:
        admins = tuple(map(lambda admin: admin.id, admins))
    return admins


async def get_members(chat_id: int, only_ids=False):
    members = await bot.get_participants(chat_id)
    if only_ids:
        members = tuple(map(lambda member: member.id, members))
    return members


async def get_command_args(commnad_message: str):
    return commnad_message.split()[1:]


async def is_user_admin(chat_id, user_id):
    chat = await db.get_chat(chat_id, ["admins"])
    return user_id in chat["admins"]


async def load_modules():
    logger.info("Started loading modules...")
    for module in ALL_MODULES:
        modulename = module.split(".")[0]
        importlib.import_module(f"bot.modules.{modulename}")
        logger.debug("Module %s imported", module)
    logger.info("All modules loaded!")


async def disconnect_bot():
    logger.info("Disconnection...")
    await bot.disconnect()
    # asyncio.get_event_loop().stop()


async def catch_up():
    logger.info("Catching up missing updates...")
    await bot.catch_up()


async def parse_identifier(string: str):
    if string.startswith("@"):
        username = string[1:]
        return username
    elif re.match("^(.*\(tg\:\/\/user\?id\=[0-9]+\))$", string):
        id_str = re.search("[0-9]+", string)[0]
        return int(id_str)


async def ban_user(chat_id, user_id):
    await db.update_chat(chat_id, {"$addToSet": {"banned": user_id}})
    await bot.edit_permissions(chat_id, user_id, view_messages=False)


async def kick_user(chat_id, user_id):
    await db.update_chat(chat_id, {"$pull": {"members": user_id}})
    await bot.edit_permissions(chat_id, user_id, view_messages=False)
    await bot.edit_permissions(chat_id, user_id)


async def unban_user(chat_id, user_id):
    await db.update_chat(chat_id, {"$pull": {"banned": user_id}})
    await bot.edit_permissions(chat_id, user_id)


async def is_user_banned(chat_id, user_id):
    chat = await db.get_chat(chat_id)
    return user_id in chat["banned"]
