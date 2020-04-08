import telethon
import asyncio
from bot import bot, logger
from bot.utils import decorators, db, utils


@decorators.smart_command("addnote", has_args=True)
@decorators.only_public
@decorators.must_be_reply(err_msg="Please a reply a message to add it as a note")
async def add_note(event):
    reply_to_id = event.message.reply_to_msg_id
    logger.debug("Loading note from %s", reply_to_id)
    reply_to_msg = await bot.get_messages(event.chat, ids=reply_to_id)
    logger.debug("Note text: %s", reply_to_msg.text)
    title = (await utils.get_command_args(event.message.raw_text))[0]
    await db.add_note_to_db(event.chat.id, title, reply_to_msg.text)
    await event.reply(f"Note {title} added!\n"
                      "Use /shownote to check text")
