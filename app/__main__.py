import asyncio
import hypercorn
import signal
import bot
import app
import sys
from app.utils import utils as app_utils
from bot.utils import utils as bot_utils


shutdown_event = asyncio.Event()


def signal_handler():
    shutdown_event.set()


@app.app.before_serving
async def startbot():
    await bot_utils.load_modules()
    if bot.config.CATCH_UP:
        await bot_utils.catch_up()


@app.app.after_serving
async def stopbot():
    await bot_utils.disconnect_bot()

asyncio.ensure_future(app_utils.load_modules())

loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, signal_handler)
loop.run_until_complete(hypercorn.asyncio.serve(
    app.app, app.hypercorn_cfg, shutdown_trigger=shutdown_event.wait))
