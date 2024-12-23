import aiofiles
import json

from . import configDir


async def getToken():
    async with aiofiles.open(f"{configDir}/token.json", "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    user_id = cache.get("user_id", None)
    token = cache.get("token", None)
    return user_id, token