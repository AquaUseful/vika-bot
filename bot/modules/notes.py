import telethon
import asyncio
from bot import bot
from bot.utils import decorators, db

@decorators.smart_command("addnote", has_args=True)
@decorators.only_public
@decorators.must_be_reply(err_msg="Please a reply a message to add it as a note")
async def add_note(event):
    pass