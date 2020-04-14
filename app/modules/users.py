import quart
import typing
from app import logger
from bot.api import users as bot_users
from app.utils import decorators, utils

blueprint = quart.Blueprint("users", __name__)


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
