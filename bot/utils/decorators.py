import functools
import telethon
from bot import bot, config, BOT_USERNAME, BOT_ID, logger
from bot.utils import db, utils


# Create telegram bot command from function
# MUST BE FIRST
# CONFLICTS WITH on_user_join, on_user_left, on_self_join, on_chat_action
def smart_command(command, has_args=False):
    def decorator(func):
        if has_args:
            pattern = f"^(?i)({config.COMMAND_PREFIX})({command})(@{BOT_USERNAME})? (.+)$"
        else:
            pattern = f"^(?i)({config.COMMAND_PREFIX})({command})(@{BOT_USERNAME})?$"
        bot.add_event_handler(func, telethon.events.NewMessage(
            incoming=True, pattern=pattern))
    return decorator


# Call function only in private messgaes with user
def only_pm(func):
    @functools.wraps(func)
    async def wrapper(event):
        if event.is_private:
            await func(event)
        else:
            await event.reply("This command available only in pm!")
    return wrapper


# Call function only in groups
def only_group(func):
    @functools.wraps(func)
    async def wrapper(event):
        if event.is_group:
            await func(event)
        else:
            await event.reply("This command is only for groups!")
    return wrapper


# Call function on any telegram event (DANGEROUS)
def raw_event():
    def decorator(func):
        bot.add_event_handler(func, telethon.events.Raw())
    return decorator


# Call function only if command is a reply to message
def must_be_reply(err_msg="This message must be a reply!"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.message.reply_to_msg_id is not None:
                await func(event)
            else:
                await event.reply(err_msg)
        return wrapper
    return decorator


# Call function only if command's sender is admin
def sender_admin(err_msg="You must be admin to do this!"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if await utils.is_user_admin(event.chat.id, event.sender.id):
                await func(event)
            else:
                await event.reply(err_msg)
        return wrapper
    return decorator


# Call function only if bot has admin privilegies
def bot_admin(err_msg="I must be admin to do this!"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if await utils.is_user_admin(event.chat.id, BOT_ID):
                await func(event)
            else:
                await event.reply(err_msg)
        return wrapper
    return decorator


# Call function when new user join
# MUST BE FIRST
# CONFLICTS WITH smart_command, on_user_left, on_self_join, on_chat_action
def on_user_join(handle_join=True, handle_add=True):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            logger.debug("User added: %s, User joined: %s",
                         event.user_added, event.user_joined)
            if (handle_join and event.user_joined) or (handle_add and event.user_added):
                await func(event)
        bot.add_event_handler(wrapper, telethon.events.ChatAction())
    return decorator


# Call function when user left
# MUST BE FIRST
# CONFLICTS WITH smart_command, on_user_join, on_self_join, on_chat_action
def on_user_left(hangle_left=True, hangle_kick=True):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if (hangle_left and event.user_left) or (hangle_kick and event.user_kicked):
                await func(event)
        bot.add_event_handler(wrapper, telethon.events.ChatAction())
    return decorator


# Call function when bot joins
# MUST BE FIRST
# CONFLICTS WITH smart_command, on_user_join, on_user_left, on_chat_action
def on_self_join(func):
    @functools.wraps(func)
    async def wrapper(event):
        if (event.user_joined or event.user_added) and (event.user is not None and event.user.id == BOT_ID):
            logger.debug("Bot joined/added to new chat (%s)", event.chat.id)
            await func(event)
    bot.add_event_handler(wrapper, telethon.events.ChatAction())


# Call function on any chat action (DANGEROUS)
# MUST BE FIRST
# CONFLICTS WITH smart_command, on_user_join, on_user_left, on_self_join
def on_chat_action(func):
    bot.add_event_handler(func, telethon.events.ChatAction())
