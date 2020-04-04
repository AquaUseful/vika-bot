import telethon
import asyncio
from bot import bot
from bot.utils import decorators, db


@decorators.smart_command("addme")
@decorators.only_private
async def addme_priv(event):
    user = event.sender
    await db.add_user_to_db(user)


@decorators.smart_command("addchat")
@decorators.only_public
async def addme_pub(event):
    chat = event.chat
    await db.add_chat_to_db(chat)
