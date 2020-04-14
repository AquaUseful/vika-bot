import quart
import functools
from bot import logger
from bot.api import tokens


def req_fields(fields: dict):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug("Testing reqest for requred fields...")
            req_json = await quart.request.json
            if fields.keys() == req_json.keys() and \
                    all(map(lambda item: isinstance(item[0], fields[item[0]]), req_json.items())):
                logger.debug("Request successfully tested")
                return await func(*args, **kwargs)
            else:
                logger.debug("Failed to test request")
                await quart.abort(400, "Request missing required fields")
        return wrapper
    return decorator


def token_verify(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        req_json = await quart.request.json
        if await tokens.verify_token(req_json["token"]):
            return await func(*args, **kwargs)
        else:
            await quart.abort(403, "Invalid token")
    return wrapper
