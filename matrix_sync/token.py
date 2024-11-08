import aiofiles
import json
import matrix_sync.config

async def getToken():
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    return cache["token"]

async def get_tip_read():
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    try:
        return cache["tip_read"]
    except KeyError:
        return False
