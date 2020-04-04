import telethon
import asyncio
from bot import bot
from bot.utils import decorators


@decorators.smart_command("ping")
@decorators.only_private
async def ping(event):
    resp = await event.respond("pong!")
