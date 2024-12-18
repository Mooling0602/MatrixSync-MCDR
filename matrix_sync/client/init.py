import json
import sys
import aiofiles
import matrix_sync.globals as globals

from . import *
from ..utils.logger import *
from ..utils.token import getToken
from nio import LoginResponse


async def cache_token(resp: LoginResponse):
    async with aiofiles.open(f"{configDir}/token.json", "w") as f:
        await f.write(json.dumps({
            "user_id": globals.config["user_id"],
            "token": resp.access_token
        }))

async def login_by_password():
    client = AsyncClient(
        get_homeserver(globals.config["homeserver"]),
        globals.config["user_id"],
        globals.config["device_id"]
    )
    resp = await client.login(globals.config["password"], device_name=globals.config["device_id"])
    if isinstance(resp, LoginResponse):
        log_info("Login by password successfully!")
        await cache_token(resp)
        log_info("Saving token of the bot account.")
    else:
        log_error(f"Failed to login your bot: {resp}")
        homeserver = get_homeserver(globals.config["homeserver"])
        log_info(f'homeserver: "{homeserver}", bot: "{globals.config["user_id"]}"')
        log_error("Please check your config, if you confirm it's correct, issue this in GitHub.")
        sys.exit(1)

async def check_token() -> bool:
    user, token = await getToken()
    if user != globals.config["user_id"]:
        log_error("The token mismatches present bot account!")
        return False
    else:
        return True