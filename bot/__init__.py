import asyncio
import logging
import telethon
import pymongo
from bot import config

logging.basicConfig(format="[%(asctime)s] (%(name)s) %(levelname)s: %(message)s",
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.info("Loading config...")
OWNER_ID = config.OWNER_ID
ADMINS = config.ADMINS
WHITELIST = config.WHITELIST + (OWNER_ID,) + ADMINS
TOKEN = config.TOKEN
NAME = TOKEN.split(":")[0]

mongo_cli = pymongo.MongoClient(config.MONGO_CONN, config.MONGO_PORT)
mongodb = mongo_cli.vika_bot

bot = telethon.TelegramClient(NAME, config.API_ID, config.API_HASH,
                              proxy=config.PROXY)
bot.start(bot_token=TOKEN)

bot_info = asyncio.get_event_loop().run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username

logger.info("Vika bot started!")
