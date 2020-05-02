import telethon
import asyncio
from bot import bot
from bot.utils import decorators


@decorators.smart_command("ping")
async def ping(event):
    resp = await event.respond("pong!")
