import telethon
import asyncio
from bot import ADMINS, bot


async def get_admins(chat_id, only_ids=False):
    admins = await bot.get_participants(chat_id, filter=telethon.tl.types.ChannelParticipantsAdmins())
    if only_ids:
        admins = tuple(map(lambda admin: admin.id, admins))
    return admins


async def get_members(chat_id, only_ids=False):
    members = await bot.get_participants(chat_id)
    if only_ids:
        members = tuple(map(lambda member: member.id, members))
    return members
