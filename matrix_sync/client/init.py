import json
import sys
import aiofiles
import matrix_sync.utils.get_logger as get_logger
import matrix_sync.plg_globals as plg_globals

from . import *
from ..utils import configDir, tr
from ..utils.token import getToken
from nio import LoginResponse


async def cache_token(resp: LoginResponse):
    async with aiofiles.open(f"{configDir}/token.json", "w") as f:
        await f.write(json.dumps({
            "user_id": plg_globals.config["user_id"],
            "token": resp.access_token
        }))

async def login_by_password():
    logger = get_logger()
    client = AsyncClient(
        get_homeserver(plg_globals.config["homeserver"]),
        plg_globals.config["user_id"],
        plg_globals.config["device_id"]
    )
    resp = await client.login(plg_globals.config["password"], device_name=plg_globals.config["device_id"])
    if isinstance(resp, LoginResponse):
        logger.info(tr("login.success"), extra={"module_name": "FirstLogin"})
        await cache_token(resp)
        plg_globals.token_vaild = True
        logger.info(tr("login.save_token"), extra={"module_name": "FirstLogin"})
    else:
        tip = tr("login.failed")
        logger.error(f"{tip}: {resp}", extra={"module_name": "FirstLogin"})
        homeserver = get_homeserver(plg_globals.config["homeserver"])
        logger.info(f'homeserver: "{homeserver}", bot: "{plg_globals.config["user_id"]}"', extra={"module_name": "FirstLogin"})
        logger.error(tr("check_config"), extra={"module_name": "FirstLogin"})
        sys.exit(1)

async def check_token() -> bool:
    user, token = await getToken()
    if user != plg_globals.config["user_id"]:
        return False
    else:
        return True