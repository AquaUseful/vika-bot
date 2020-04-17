import telethon
from bot import bot, logger
from bot.utils import decorators, db, utils


async def ban_user(chat_id, user_id):
    await bot.edit_permissions(chat_id, user_id, view_messages=False)


@decorators.smart_command("ban", has_args=True)
@decorators.sender_admin()
@decorators.bot_admin()
async def ban_user_by_username(event):
    firstarg = (await utils.get_command_args(event.message.text))[0]
    logger.debug("Trying to ban: %s", firstarg)
