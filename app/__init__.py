import quart
import os

app = quart.Quart(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
