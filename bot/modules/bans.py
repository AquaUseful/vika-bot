import telethon
from bot import bot, logger
from bot.utils import decorators, db, utils


@decorators.smart_command("ban", has_args=True)
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    if await utils.is_user_banned(event.chat.id, user.id):
        await event.reply("This user is already banned!")
    elif await utils.is_user_admin(event.chat.id, user.id):
        await event.reply("I can't ban admins!")
    else:
        await utils.ban_user(event.chat.id, user.id)
        await bot.send_message(event.chat, f"{user.first_name} banned by {event.message.sender.first_name}")


@decorators.smart_command("ban")
@decorators.sender_admin()
@decorators.bot_admin()
@decorators.must_be_reply()
async def ban_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    if await utils.is_user_banned(event.chat.id, reply_sender.id):
        await event.reply("This user is already banned!")
    elif await utils.is_user_admin(event.chat.id, reply_sender.id):
        await event.reply("I can't ban admins!")
    else:
        await utils.ban_user(event.chat.id, reply_sender.id)
        await bot.send_message(event.chat, f"{reply_sender.first_name} banned by {event.message.sender.first_name}")


@decorators.smart_command("unban", has_args=True)
@decorators.sender_admin()
@decorators.bot_admin()
async def unban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    if await utils.is_user_banned(event.chat.id, user.id):
        await utils.unban_user(event.chat.id, user.id)
        await bot.send_message(event.chat, f"{user.first_name} unbanned by {event.message.sender.first_name}")
    else:
        await event.reply("This user is not banned!")


@decorators.smart_command("unban")
@decorators.sender_admin()
@decorators.bot_admin()
@decorators.must_be_reply()
async def unban_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    if await utils.is_user_banned(event.chat.id, reply_sender.id):
        await utils.unban_user(event.chat.id, reply_sender.id)
        await bot.send_message(event.chat, f"{reply_sender.first_name} unbanned by {event.message.sender.first_name}")
    else:
        await event.reply("This user is not banned!")
