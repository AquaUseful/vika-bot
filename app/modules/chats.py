import quart
from app.utils import decorators
from bot.api import tokens as bot_tokens
from bot.api import users as bot_users

blueprint = quart.Blueprint("chats", __name__)


@blueprint.route("/api/chats/user_ids", methods=["POST"])
@decorators.req_fields({"token": str})
@decorators.token_verify
async def user_list():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    users = await bot_users.get_chat_members(chat_id)
    return quart.jsonify({
        "users": users
    })

@blueprint.route("/api/chats/title")
@decorators.req_fields({"token": str})
@decorators.token_verify
async def title():
    req_json = await quart.request.json
    