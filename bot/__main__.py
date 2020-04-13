import asyncio
import signal
import sys
from bot import config, logger, bot
from bot.utils import utils

asyncio.ensure_future(utils.load_modules())

if config.CATCH_UP:
    logger.info("Catching missed updates")
    asyncio.ensure_future(utils.catch_up())

async def exit_gracefully():
    await utils.disconnect_bot()
    logger.info("Disconnected, stopping...")
    asyncio.get_event_loop().stop()

def signal_handler(signal, frame):
    asyncio.ensure_future(exit_gracefully())

signal.signal(signal.SIGINT, signal_handler)
logger.debug("Interrupt signal set")
logger.info("Starting main event loop...")
asyncio.get_event_loop().run_forever()
