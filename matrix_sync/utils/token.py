import aiofiles
import json

from .. import config

async def getToken():
    TOKEN_FILE = config.TOKEN_FILE
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    user_id = cache.get("user_id", None)
    token = cache.get("token", None)
    return user_id, token