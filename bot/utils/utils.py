import telethon
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
from bot import ADMINS, bot
from bot.utils import db


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


async def is_user_admin(chat_id: int, user_id: int):
    return user_id in db.get_chat(chat_id, ["admins"])


async def get_command_args(commnad_message: str):
    return commnad_message.split()[1:]


async def is_user_admin(chat_id, user_id):
    chat = await db.get_chat(chat_id, ["admins"])
    return user_id in chat["admins"]
