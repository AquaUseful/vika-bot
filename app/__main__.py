import asyncio
import hypercorn
import signal
import bot
import app
import sys
from app import config, app
from app.utils import blueprints
from bot.utils import utils as bot_utils


shutdown_event = asyncio.Event()


def signal_handler():
    shutdown_event.set()


# Start bot before starting app
@app.before_serving
async def startup():
    await bot_utils.load_modules()
    if bot.config.CATCH_UP:
        await bot_utils.catch_up()


# Disable bot before stopping app
@app.after_serving
async def shutdown():
    await bot_utils.disconnect_bot()

# Load all modules
asyncio.ensure_future(blueprints.register_blueprints())

# Initialise server
hypercorn_cfg = hypercorn.Config()
hypercorn_cfg.bind = [f"{config.HOST}:{config.PORT}",
                      f"[{config.HOST_IPV6}]:{config.PORT}"]


loop = asyncio.get_event_loop()

# Connect SIGINT to shutdown
loop.add_signal_handler(signal.SIGINT, signal_handler)

loop.run_until_complete(hypercorn.asyncio.serve(
    app, hypercorn_cfg, shutdown_trigger=shutdown_event.wait))
