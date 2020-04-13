import quart
import functools
from bot.api import tokens


def req_fields(fields):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            req_json = quart.request.json
            if all(map(lambda field: field in req_fields, fields)):
                return await func(*args, **kwargs)
            else:
                await quart.abort(400, "Request missing required fields")


def token_verify(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        req_json = quart.request.json
        if tokens.verify_token(req_json["token"]):
            return await func(*args, **kwargs)
        else:
            await quart.abort(403, "Invalid token")
