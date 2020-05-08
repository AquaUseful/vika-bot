from bot.utils import decorators


@decorators.smart_command("help")
async def help(event):
    help_msg = """HELP MESSAGE:

/help - display this message

/ping - test connecion to bot

/addnote - add save message as note to database (must be a reply)

/shownote <note name> - show saved note

/delnote <note name> - delete note from database

/notes - list all notes from current chat

/kick [username] - kick user from chat (when used as a reply kicks origin's sender)

/ban [username] - bans user in this chat (when used as a reply bans origin's sender)

/unban [username] - removes user from ban list (when used as a reply unbans origin's sender)

/promote [username] - gives admin privilege to user in this chat (when used as a reply promotes origin's sender)

/demote [username] - revokes admin privilege from user in this chat (when used as a reply demotes origin's sender)

/update - updates chat data in database (use in case of errors)

/token - use for token operations (has its own help)
"""
    await event.reply(help_msg)
