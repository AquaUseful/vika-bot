import telethon
import asyncio
from bot import bot
from bot.utils import decorators


@decorators.smart_command("ping")
async def ping(event):
    await event.respond("pong!")
