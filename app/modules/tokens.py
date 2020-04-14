import quart
from bot.api import tokens as bot_tokens
from app.utils import decorators

blueprint = quart.Blueprint("tokens", __name__)


@blueprint.route("/api/tokens/verify", methods=["POST"])
@decorators.req_fields({"token": str})
async def token_verify():
    json_resp = await quart.request.json
    token = json_resp["token"]
    result = bot_tokens.verify_token(token)
    return quart.jsonify({"result": result})