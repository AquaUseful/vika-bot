import asyncio
import telethon
import pymongo
import importlib
import sys
import signal
from bot import config, logger, bot
from bot.modules import ALL_MODULES

logger.info("Started loading modules...")
for module in ALL_MODULES:
    modulename = module.split(".")[0]
    importlib.import_module(f"bot.modules.{modulename}")
    logger.debug("Module %s imported", module)
logger.info("All modules loaded!")

if config.CATCH_UP:
    logger.info("Catching missed updates")
    asyncio.ensure_future(bot.catch_up())


def stop_bot(signal, frame):
    logger.debug(signal)
    logger.info("Stopping bot...")
    sys.exit()


signal.signal(signal.SIGINT, stop_bot)
logger.debug("Interrupt signal set")
logger.info("Starting main event loop...")
asyncio.get_event_loop().run_forever()
