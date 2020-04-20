import quart
from app.utils import decorators
from bot.api import tokens as bot_tokens
from bot.api import bans as bot_bans

blueprint = quart.Blueprint("bans", __name__)


@blueprint.route("/api/bans/ban", methods=["POST"])
@decorators.req_fields({"token": str, "user_id": int})
@decorators.token_verify
async def ban_user():
    req_json = await quart.request.json
    token = req_json["token"]
    chat_id = await bot_tokens.get_chat_id_by_token(token)
    result = await bot_bans.ban_user(chat_id, req_json["user_id"])
    return quart.jsonify({"result": result})
