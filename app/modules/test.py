import asyncio
import quart
from app import app


@app.route("/")
async def root():
    return "test"
