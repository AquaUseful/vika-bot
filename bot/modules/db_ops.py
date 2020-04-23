from bot import logger
from bot.utils import decorators, db, utils


@decorators.on_self_join
async def add_chat(event):
    chat = event.chat
    await db.add_chat_to_db(chat)


@decorators.on_chat_action
async def update_chat(event):
    logger.debug("Got chat action, updating info...")
    members = utils.get_members(event.chat.id, only_ids=True)
    admins = utils.get_admins(event.chat.id, only_ids=True)
    banned = utils.get_banned(event.chat_id, only_ids=True)
    await db.update_chat(event.chat.id, {"$set": {"members": members,
                                                  "admins": admins,
                                                  "banned": banned}})
