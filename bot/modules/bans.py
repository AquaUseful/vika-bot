import telethon
from bot import bot, logger
from bot.utils import decorators, db, utils


# Performs all check and ban user is all is ok
async def ban_check(chat: telethon.types.Chat, user: telethon.types.User, cmd_msg: telethon.types.Message):
    if await utils.is_user_banned(chat.id, user.id):
        await bot.send_message(message="This user is already banned!", entity=chat, reply_to=cmd_msg)
    elif await utils.is_user_admin(chat.id, user.id):
        await bot.send_message(message="I can't ban admins!", entity=chat, reply_to=cmd_msg)
    else:
        try:
            await utils.ban_user(chat.id, user.id)
            await bot.send_message(message=f"{user.first_name} banned by {cmd_msg.sender.first_name}", entity=chat, reply_to=cmd_msg)
        except telethon.errors.ChatAdminRequiredError:
            await bot.send_message(message="I have no permissions to do this!", entity=chat, reply_to=cmd_msg)


@decorators.smart_command("ban", has_args=True)
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    await ban_check(event.chat, user, event.message)


@decorators.smart_command("ban")
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
@decorators.must_be_reply()
async def ban_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    await ban_check(event.chat, reply_sender, event.message)


# Perform all checks and unban user is all is ok
async def unban_check(chat: telethon.types.Chat, user: telethon.types.User, cmd_msg: telethon.types.Message):
    if await utils.is_user_banned(chat.id, user.id):
        try:
            await utils.unban_user(chat.id, user.id)
            await bot.send_message(message=f"{user.first_name} unbanned by {cmd_msg.sender.first_name}", entity=chat, reply_to=cmd_msg)
        except telethon.errors.ChatAdminRequiredError:
            await bot.send_message(message="I have no permissions to do this!", entity=chat, reply_to=cmd_msg)
    else:
        await bot.send_message(message="This user is not banned!", entity=chat, reply_to=cmd_msg)


@decorators.smart_command("unban", has_args=True)
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
async def unban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    await unban_check(event.chat, user, event.message)


@decorators.smart_command("unban")
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
@decorators.must_be_reply()
async def unban_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    await unban_check(event.chat, reply_sender, event.message)
