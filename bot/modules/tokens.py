import secrets
import pymongo
from bot import bot, config
from bot.utils import db, decorators, utils


async def set_new_token(chat_id):
    while True:
        token = secrets.token_urlsafe(config.ACCESS_TOKEN_SIZE)
        chat = await db.get_chat_by_token(token, ["tg_id"])
        if chat and chat["tg_id"] != chat_id:
            continue
        break
    await db.update_chat(chat_id, {"$set": {"token": token}})
    return token


async def has_token(chat_id):
    token = (await db.get_chat(chat_id, ["token"]))["token"]
    return token is not None


async def revoke_token(chat_id):
    await db.update_chat(chat_id, {"$set": {"token": None}})


async def get_token(chat_id):
    token = (await db.get_chat(chat_id, ["token"]))["token"]
    return token


@decorators.smart_command("token", has_args=True)
@decorators.only_public
@decorators.sender_admin()
@decorators.bot_admin()
async def token(event):
    action = (await utils.get_command_args(event.message.raw_text))[0].lower()
    if action == "get":
        if not await has_token(event.chat.id):
            token = await set_new_token(event.chat.id)
        else:
            token = await get_token(event.chat.id)
        sender = event.sender
        await bot.send_message(sender, f"Get yout token for {event.chat.title}:\n\n{token}")
    elif action == "revoke":
        await revoke_token(event.chat.id)
        await event.reply("Current token for chat has revoken, use 'new' or 'get' param to set new")
    elif action == "new":
        await set_new_token(event.chat.id)
        await event.reply("New token for this chat set, use 'get' to reveal")


@decorators.smart_command("token")
@decorators.only_public
@decorators.sender_admin()
@decorators.bot_admin()
async def token_help(event):
    await event.reply("Control access token (for admins):\n"
                      "get - get acces token to your pm\n"
                      "revoke - revoke current tokeb\n"
                      "new - create a new token (overwrites current if exists)")
