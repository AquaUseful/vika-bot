import quart
import quart.flask_patch
import hypercorn
import os

hypercorn_cfg = hypercorn.Config()
app = quart.Quart(__name__)
app.config.secret_key = os.urandom(32)
