import quart
import os
import logging

logging.basicConfig(format="[%(asctime)s] (%(name)s) %(levelname)s: %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = quart.Quart(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
