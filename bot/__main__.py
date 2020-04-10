import asyncio
import signal
from bot import config, logger, bot
from bot.utils import utils

asyncio.ensure_future(utils.load_modules())

if config.CATCH_UP:
    logger.info("Catching missed updates")
    asyncio.ensure_future(utils.catch_up())


def exit_gracefully(signal, frame):
    asyncio.ensure_future(utils.disconnect_bot())
    logger.info("Disconnected, stopped")
    asyncio.get_event_loop().stop()


signal.signal(signal.SIGINT, exit_gracefully)
logger.debug("Interrupt signal set")
logger.info("Starting main event loop...")
asyncio.get_event_loop().run_forever()
