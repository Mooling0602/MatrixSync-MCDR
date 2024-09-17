import aiofiles
import json
import matrix_sync.config

async def getToken():
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    return cache["token"]