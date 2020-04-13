import app
from app.modules import users


async def register_blueprints():
    await app.app.register_blueprint(users.blueprint)
