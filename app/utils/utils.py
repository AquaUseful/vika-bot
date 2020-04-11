import importlib
from app.modules import ALL_MODULES
from bot import logger


async def load_modules():
    logger.info("Started loading modules...")
    for module in ALL_MODULES:
        modulename = module.split(".")[0]
        importlib.import_module(f"app.modules.{modulename}")
        logger.debug("Module %s imported", module)
    logger.info("All modules loaded!")
