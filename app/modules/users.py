import quart
from bot.api import users as bot_users
from bot.api import tokens as bot_tokens
from app.utils import decorators

blueprint = quart.Blueprint(__name__, __name__)


@blueprint.route("/api/users", methods=["POST"])
@decorators.req_fields(["token"])
@decorators.token_verify
async def user_list():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    users = await bot_users.get_chat_members(chat_id)
    return quart.jsonify({
        "users": users
    })
