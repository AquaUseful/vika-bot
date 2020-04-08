import telethon
import asyncio
from bot import bot, logger, mongodb
from bot.utils import decorators
from telethon.tl.types import MessageActionChatMigrateTo


@decorators.raw_event()
async def migrate_chat(event):
    if hasattr(event, "message") and isinstance(event.message.action, MessageActionChatMigrateTo):
        old_id = event.message.to_id.chat_id
        new_id = event.message.action.channel_id
        logger.debug("Chat %s migrated to id %s", old_id, new_id)
        res = mongodb.chats.update_one(
            {"tg_id": old_id}, {"$set": {"tg_id": new_id}})
        logger.debug(res)
