from bot.utils import decorators, db


@decorators.on_self_join
async def add_chat(event):
    chat = event.chat
    await db.add_chat_to_db(chat)
