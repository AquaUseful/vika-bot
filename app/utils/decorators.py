import quart
import functools
from bot import logger
from bot.api import tokens


# Check request's json for field names and types
def req_fields(fields: dict):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug("Testing reqest for requred fields...")
            req_json = await quart.request.json
            if fields.keys() == req_json.keys() and \
                    all(map(lambda item: isinstance(item[1], fields[item[0]]), req_json.items())):
                logger.debug("Request successfully tested")
                return await func(*args, **kwargs)
            else:
                logger.debug("Failed to test request")
                await quart.abort(400, "Request missing required fields")
        return wrapper
    return decorator


# Call function only when token is valid
# MUST be used with req_fields check for token field
def token_verify(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        req_json = await quart.request.json
        if await tokens.verify_token(req_json["token"]):
            return await func(*args, **kwargs)
        else:
            await quart.abort(403, "Invalid token")
    return wrapper
