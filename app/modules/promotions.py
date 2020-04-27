import quart
from app.utils import decorators
from bot.api import promotions as bot_promotions
from bot.api import tokens as bot_tokens

blueprint = quart.Blueprint("promotions", __name__)


@blueprint.route("/api/promotions/promote", methods=["POST"])
@decorators.req_fields({"token": str, "user_id": int})
@decorators.token_verify
async def ban_user():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    result = await bot_promotions.promote_user(chat_id, req_json["user_id"])
    return quart.jsonify({"result": result})


@blueprint.route("/api/promotions/demote", methods=["POST"])
@decorators.req_fields({"token": str, "user_id": int})
@decorators.token_verify
async def unban_user():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    result = await bot_promotions.demote_user(chat_id, req_json["user_id"])
    return quart.jsonify({"result": result})
