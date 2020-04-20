from app import app
from app.modules import users, chats, tokens, bans


async def register_blueprints():
    app.register_blueprint(users.blueprint)
    app.register_blueprint(chats.blueprint)
    app.register_blueprint(tokens.blueprint)
    app.register_blueprint(bans.blueprint)
