import quart
import typing
from bot import logger
from bot.api import users as bot_users
from bot.api import tokens as bot_tokens
from app.utils import decorators, utils

blueprint = quart.Blueprint(__name__, __name__)


@blueprint.route("/api/chat/get_user_ids", methods=["POST"])
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


@blueprint.route("/api/users/getinfo", methods=["POST"])
@decorators.req_fields({"ids": typing.Iterable})
async def get_user():
    req_json = await quart.request.json
    try:
        users = await bot_users.get_users_info(req_json["ids"])
    except ValueError as exc:
        await quart.abort(400, exc)
    user_dict = {user.id: {item[0]: item[1] for item in vars(user).items() if utils.is_jsonable(item[1])}
                 for user in users}
    return quart.jsonify(user_dict)
