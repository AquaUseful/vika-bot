import asyncio
import hypercorn
import signal
import bot
from app import app
from app import config
from bot.utils import utils

shutdown_event = asyncio.Event()


def signal_handler():
    shutdown_event.set()


@app.before_serving
async def startbot():
    await bot.utils.utils.load_modules()
    if bot.config.CATCH_UP:
        await bot.utils.utils.catch_up()


@app.after_serving
async def stopbot():
    await bot.utils.utils.disconnect_bot()


hypercorn_cfg = hypercorn.Config()


loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, signal_handler)
loop.run_until_complete(hypercorn.asyncio.serve(
    app, hypercorn_cfg, shutdown_trigger=shutdown_event.wait))
