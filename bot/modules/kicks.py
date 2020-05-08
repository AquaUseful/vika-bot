import telethon
from bot import bot, logger
from bot.utils import decorators, utils, db


# Perform all checks and kick user is all is ok
async def check_kick(chat: telethon.types.Chat, user: telethon.types.User, cmd_msg: telethon.types.Message):
    if await utils.is_user_admin(chat.id, user.id):
        await bot.send_message(message="I can't kick admins!", entity=chat, reply_to=cmd_msg)
    else:
        try:
            await utils.kick_user(chat.id, user.id)
            await bot.send_message(message=f"{user.first_name} kicked by {cmd_msg.sender.first_name}", entity=chat, reply_to=cmd_msg)
        except telethon.errors.ChatAdminRequiredError:
            await bot.send_message(message="I have no permissions to do this!", entity=chat, reply_to=cmd_msg)


@decorators.smart_command("kick", has_args=True)
@decorators.only_group
@decorators.sender_admin()
@decorators.bot_admin()
async def kick_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    user_identifier = await utils.parse_identifier(firstarg)
    user = await bot.get_entity(user_identifier)
    logger.debug("Trying to ban: %s", user.id)
    await check_kick(event.chat, user, event.message)


@decorators.smart_command("kick")
@decorators.only_group
@decorators.must_be_reply()
@decorators.sender_admin()
@decorators.bot_admin()
async def kick_user_by_message(event):
    reply_to_msg = await event.message.get_reply_message()
    reply_sender = reply_to_msg.sender
    logger.debug("Trying to ban %s", reply_sender.id)
    await check_kick(event.chat, reply_sender, event.message)
