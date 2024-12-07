import aiofiles
import json

from .. import config

async def getToken():
    TOKEN_FILE = config.TOKEN_FILE
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    return cache["user_id"], cache["token"]