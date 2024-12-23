import json
import sys
import aiofiles
import matrix_sync.plg_globals as plg_globals

from . import *
from ..utils.logger import *
from ..utils.token import getToken
from nio import LoginResponse


async def cache_token(resp: LoginResponse):
    async with aiofiles.open(f"{configDir}/token.json", "w") as f:
        await f.write(json.dumps({
            "user_id": plg_globals.config["user_id"],
            "token": resp.access_token
        }))

async def login_by_password():
    client = AsyncClient(
        get_homeserver(plg_globals.config["homeserver"]),
        plg_globals.config["user_id"],
        plg_globals.config["device_id"]
    )
    resp = await client.login(plg_globals.config["password"], device_name=plg_globals.config["device_id"])
    if isinstance(resp, LoginResponse):
        log_info(tr("login.success"))
        await cache_token(resp)
        log_info(tr("login.save_token"))
    else:
        tip = tr("login.failed")
        log_error(f"{tip}: {resp}")
        homeserver = get_homeserver(plg_globals.config["homeserver"])
        log_info(f'homeserver: "{homeserver}", bot: "{plg_globals.config["user_id"]}"')
        log_error(tr("check_config"))
        sys.exit(1)

async def check_token() -> bool:
    user, token = await getToken()
    if user != plg_globals.config["user_id"]:
        log_error(tr("token_mismatch"))
        return False
    else:
        return True