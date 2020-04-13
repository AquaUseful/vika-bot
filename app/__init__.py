import quart
import hypercorn
import os

hypercorn_cfg = hypercorn.Config()
app = quart.Quart(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
