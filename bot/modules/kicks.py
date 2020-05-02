import telethon
from bot import bot, logger
from bot.utils import decorators, utils, db


@decorators.smart_command("kick", has_args=True)
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    if await utils.is_user_admin(event.chat.id, user.id):
        await event.reply("I can't kick admins!")
    else:
        try:
            await utils.kick_user(event.chat.id, user.id)
            await bot.send_message(event.chat, f"{user.first_name} kicked by {event.message.sender.first_name}")
        except telethon.errors.ChatAdminRequiredError:
            await event.reply("I have no permissions to do this!")


@decorators.smart_command("kick")
@decorators.only_group
@decorators.must_be_reply()
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    if await utils.is_user_admin(event.chat.id, reply_sender.id):
        await event.reply("I can't kick admins!")
    else:
        try:
            await utils.kick_user(event.chat.id, reply_sender.id)
            await bot.send_message(event.chat, f"{reply_sender.first_name} kicked by {event.message.sender.first_name}")
        except telethon.errors.ChatAdminRequiredError:
            await event.reply("I have no permissions to do this!")
