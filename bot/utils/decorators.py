import functools
import telethon
from bot import bot, config, BOT_USERNAME, DEF_LANG


def smart_command(command, has_args=False, no_pm=False, no_public=False):
    def decorator(func):
        if has_args:
            pattern = f"^(?i)({config.COMMAND_PREFIX})({command}) (.+)$"
        else:
            pattern = f"^(?i)({config.COMMAND_PREFIX})({command})$"
        bot.add_event_handler(func, telethon.events.NewMessage(
            incoming=True, pattern=pattern))
    return decorator


def only_private(func):
    @functools.wraps(func)
    async def wrapper(event):
        if event.is_private:
            await func(event)
        else:
            await event.reply("This command available only in private chats!")
    return wrapper


def client_is_admin(client: telethon.TelegramClient):
    pass
