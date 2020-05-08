import telethon
from bot import bot, logger, BOT_ID
from bot.utils import utils, decorators


# Performs all checks and promotes user is all is ok
async def promote_check(chat: telethon.types.Chat, user: telethon.types.User, cmd_msg: telethon.types.Message):
    if await utils.is_user_admin(chat.id, user.id):
        await bot.send_message(message="This user is already admin!", entity=chat, reply_to=cmd_msg)
    else:
        try:
            await utils.promote_user(chat.id, user.id)
            await bot.send_message(message=f"{user.first_name} promoted by {cmd_msg.sender.first_name}", entity=chat, reply_to=cmd_msg)
        except telethon.errors.BotChannelsNaError:
            await bot.send_message(message="Sorry, I can't promote users!", entity=chat, reply_to=cmd_msg)


@decorators.smart_command("promote", has_args=True)
@decorators.only_group
@decorators.bot_admin()
@decorators.sender_admin()
async def promote_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to promote: %s", user.id)
    await promote_check(event.chat, user, event.message)


@decorators.smart_command("promote")
@decorators.only_group
@decorators.must_be_reply()
@decorators.bot_admin()
@decorators.sender_admin()
async def promote_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to promote %s", reply_sender.id)
    await promote_check(event.chat, reply_sender, event.message)


# Perform all checks and demote user is all is ok
async def demote_check(chat: telethon.types.Chat, user: telethon.types.User, cmd_msg: telethon.types.Message):
    if cmd_msg.sender == user:
        await bot.send_message(message="You can't demote yourself!", entity=chat, reply_to=cmd_msg)
    elif user.id == BOT_ID:
        await bot.send_message(message="I can't demote myself!", entity=chat, reply_to=cmd_msg)
    elif await utils.is_user_admin(chat.id, user.id):
        try:
            await utils.demote_user(chat.id, user.id)
            await bot.send_message(message=f"{user.first_name} demoted by {cmd_msg.sender.first_name}", entity=chat, reply_to=cmd_msg)
        except telethon.errors.BotChannelsNaError:
            await bot.send_message(message=f"Sorry, I can't demote users!", entity=chat, reply_to=cmd_msg)
    else:
        await bot.send_message(message=f"{user.first_name} is not admin!", entity=chat, reply_to=cmd_msg)


@decorators.smart_command("demote", has_args=True)
@decorators.only_group
@decorators.bot_admin()
@decorators.sender_admin()
async def demote_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to promote: %s", user.id)
    await demote_check(event.chat, user, event.message)


@decorators.smart_command("demote")
@decorators.only_group
@decorators.must_be_reply()
@decorators.bot_admin()
@decorators.sender_admin()
async def demote_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to promote %s", reply_sender.id)
    await demote_check(event.chat, reply_sender, event.message)
