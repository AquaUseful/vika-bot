import telethon
from bot import bot, logger
from bot.utils import decorators, db, utils


@decorators.smart_command("ban", has_args=True)
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user_id = (await bot.get_entity(user_identifier)).id
    logger.debug("Trying to ban: %s", user_id)
    if await utils.is_user_admin(event.chat.id, user_id):
        await event.reply("I can't ban admins!")
    else:
        await bot.edit_permissions(event.chat, user_id, view_messages=False)


@decorators.smart_command("ban")
@decorators.sender_admin()
@decorators.bot_admin()
@decorators.must_be_reply()
async def ban_user_by_message(event):
    reply_to_id = event.message.reply_to_msg_id
    reply_to_msg = await bot.get_messages(event.chat, ids=reply_to_id)
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    if await utils.is_user_admin(event.chat.id, reply_sender.id):
        await event.reply("I can't ban admins!")
    else:
        await bot.edit_permissions(event.chat, reply_sender, view_messages=False)
