from bot import logger, bot
from bot.utils import decorators, db, utils


@decorators.on_self_join
async def add_chat(event):
    chat = event.chat
    await db.add_chat_to_db(chat)
    await bot.send_message(event.chat, "Hello! I'm Vika bot and i will help admins!"
                           "You must give me all admin rights and use /update after that.")


async def update_chat(event):
    logger.debug("Got chat action, updating info...")
    members = await utils.get_members(event.chat.id, only_ids=True)
    admins = await utils.get_admins(event.chat.id, only_ids=True)
    banned = await utils.get_banned(event.chat_id, only_ids=True)
    await db.update_chat(event.chat.id, {"$set": {"members": members,
                                                  "admins": admins,
                                                  "banned": banned}})


@decorators.smart_command("update")
@decorators.only_group
async def update_chat_cmd(event):
    await update_chat(event)
    await bot.send_message(event.chat, "Chat data updated")


@decorators.on_chat_action
async def update_chat_act(event):
    await update_chat(event)
