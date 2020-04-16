import quart
from app.utils import decorators, utils
from bot.api import tokens as bot_tokens
from bot.api import users as bot_users
from bot.api import chats as bot_chats

blueprint = quart.Blueprint("chats", __name__)


@blueprint.route("/api/chats/users", methods=["POST"])
@decorators.req_fields({"token": str})
@decorators.token_verify
async def users():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    users = await bot_chats.get_chat_members(chat_id)
    user_dict = {user.id: {item[0]: item[1] for item in vars(user).items() if utils.is_jsonable(item[1])}
                 for user in users}
    return quart.jsonify(user_dict)


@blueprint.route("/api/chats/info", methods=["POST"])
@decorators.req_fields({"token": str})
@decorators.token_verify
async def title():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    chat = await bot_chats.get_chat_info(chat_id)
    return quart.jsonify(chat)
