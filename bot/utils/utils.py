import telethon
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
from bot import ADMINS, bot
from bot.utils import db


async def get_admins(chat_id: int, only_ids=False):
    admins = await bot.get_participants(chat_id, filter=ChannelParticipantsAdmins)
    print(admins)
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
