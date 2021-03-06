import asyncio
import logging
import telethon
import pymongo
import os
from motor import motor_asyncio
from bot import config

logging.basicConfig(format="[%(asctime)s] (%(name)s) %(levelname)s: %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Loading config...")
OWNER_ID = config.OWNER_ID
TOKEN = config.TOKEN
NAME = TOKEN.split(":")[0]

# Use mongo uri from environment if running on heroku
if "IS_HEROKU" in os.environ:
    mongo_cli = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URI"])
else:
    mongo_cli = motor_asyncio.AsyncIOMotorClient(config.MONGO_URI)

# Initialising database
mongodb = mongo_cli.vika_bot
if config.INIT_DB:
    logger.info("Initialising db indexes")
    asyncio.gather(
        mongodb.users.create_index(
            [("tg_id", pymongo.ASCENDING)], unique=True),
        mongodb.chats.create_index(
            [("tg_id", pymongo.ASCENDING)], unique=True),
        mongodb.chats.create_index([("token", pymongo.HASHED)]),
        mongodb.notes.create_index([("chat_id", pymongo.ASCENDING), ("title", pymongo.ASCENDING)], unique=True))

# Initialising bot
bot = telethon.TelegramClient(NAME, config.API_ID, config.API_HASH,
                              proxy=config.PROXY)
bot.start(bot_token=TOKEN)

bot_info = asyncio.get_event_loop().run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_ID = bot_info.id

logger.info("Vika bot started!")
