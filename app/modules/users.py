import quart
import typing
from app import logger
from bot.api import users as bot_users
from app.utils import decorators, utils

blueprint = quart.Blueprint("users", __name__)


@blueprint.route("/api/users/info", methods=["POST"])
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


@blueprint.route("/api/users/<int:user_id>/photo", methods=["GET"])
async def photo(user_id):
    photo = await bot_users.get_last_photo(user_id)
    if photo is None:
        await quart.abort(404)
    resp = await quart.make_response(photo)
    resp.headers.set("Content-Type", "image/jpeg")
    resp.headers.set("Content-Disposition", "attachment",
                     filename=f"{user_id}.jpeg")
    return resp
