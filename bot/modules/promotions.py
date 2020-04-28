import telethon
from bot import bot, logger, BOT_ID
from bot.utils import utils, decorators


@decorators.smart_command("promote", has_args=True)
@decorators.bot_admin()
@decorators.sender_admin()
async def promote_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to promote: %s", user.id)
    if await utils.is_user_admin(event.chat.id, user.id):
        await event.reply("This user is already admin!")
    else:
        try:
            await utils.promote_user(event.chat.id, user.id)
            await bot.send_message(event.chat, f"{user.first_name} promoted by {event.message.sender.first_name}")
        except telethon.errors.BotChannelsNaError:
            await event.reply("Sorry, I can't promote users!")


@decorators.smart_command("promote")
@decorators.must_be_reply()
@decorators.bot_admin()
@decorators.sender_admin()
async def promote_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to promote %s", reply_sender.id)
    if await utils.is_user_admin(event.chat.id, reply_sender.id):
        await event.reply("This user is already admin")
    else:
        try:
            await utils.promote_user(event.chat.id, reply_sender.id)
            await bot.send_message(event.chat, f"{reply_sender.first_name} promoted by {event.message.sender.first_name}")
        except telethon.errors.BotChannelsNaError:
            await event.reply("Sorry, I can't promote users!")


@decorators.smart_command("demote", has_args=True)
@decorators.bot_admin()
@decorators.sender_admin()
async def demote_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to promote: %s", user.id)
    if event.sender == user:
        await event.reply("You can't demote yourself!")
    elif user.id == BOT_ID:
        await event.reply("I can't demote myself!")
    elif await utils.is_user_admin(event.chat.id, user.id):
        try:
            await utils.demote_user(event.chat.id, user.id)
            await event.reply(f"{user.first_name} demoted by {event.message.sender.first_name}")
        except telethon.errors.BotChannelsNaError:
            await event.reply(f"Sorry, I can't demote users!")
    else:
        await event.reply(f"{user.first_name} is not admin!")


@decorators.smart_command("demote")
@decorators.must_be_reply()
@decorators.bot_admin()
@decorators.sender_admin()
async def demote_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to promote %s", reply_sender.id)
    if event.sender == reply_sender:
        await event.reply("You can't demote yourself!")
    elif reply_sender == BOT_ID:
        await event.reply("I can't demote myself!")
    elif await utils.is_user_admin(event.chat.id, reply_sender.id):
        try:
            await utils.demote_user(event.chat.id, reply_sender.id)
            await event.reply(f"{reply_sender.first_name} demoted by {event.message.sender.first_name}")
        except telethon.errors.BotChannelsNaError:
            await event.reply(f"Sorry, I can't demote users!")
    else:
        await event.reply(f"{reply_sender.first_name} is not admin!")
