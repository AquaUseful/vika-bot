import telethon
import asyncio
from bot import bot, logger
from bot.utils import decorators, db, utils


@decorators.smart_command("setwelcome", has_args=True)
@decorators.only_group
@decorators.sender_admin()
async def set_welcome(event):
    title = (await utils.get_command_args(event.message.raw_text))[0]
    note = await db.get_note(event.chat.id, title)
    if note:
        await db.update_chat(event.chat.id, {"$set": {"welcome": note["_id"]}})
        await event.reply(f"Note {title} set as welcome")
    else:
        await event.reply(f"Note {title} not found")


@decorators.on_user_join()
async def send_welcome(event):
    logger.debug("New user joined, trying to get note...")
    note_id = (await db.get_chat(event.chat.id, ["welcome"]))["welcome"]
    logger.debug("Note id: %s", note_id)
    if note_id:
        logger.debug("Welcome note get, trying to greet user")
        user_fname = (await event.get_user()).first_name
        note_text = (await db.get_note_by_id(note_id, ["text"]))["text"]
        await bot.send_message(event.chat, note_text.format(uname=user_fname))
