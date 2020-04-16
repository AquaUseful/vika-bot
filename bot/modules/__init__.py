from bot import logger
import os
import glob


def get_all_modules():
    modules = glob.glob(f"{os.path.dirname(__file__)}/*.py")
    all_modules = tuple(map(lambda mod: os.path.basename(mod), filter(
        lambda mod: not mod.endswith("__init__.py"), modules)))
    return all_modules


ALL_MODULES = get_all_modules()
logger.info("Found modules: %s", str(ALL_MODULES))
__all__ = ALL_MODULES
