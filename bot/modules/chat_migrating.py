import telethon
import asyncio
from bot import bot, logger
from bot.utils import decorators, db
from telethon.tl.types import MessageActionChatMigrateTo

# Change db when chat transforms from group to megagroup
@decorators.raw_event()
async def migrate_chat(event):
    if hasattr(event, "message") and isinstance(event.message.action, MessageActionChatMigrateTo):
        old_id = event.message.to_id.chat_id
        new_id = event.message.action.channel_id
        logger.info("Chat %s migrated to id %s", old_id, new_id)
        await db.change_chat_id(old_id, new_id)
