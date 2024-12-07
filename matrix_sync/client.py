import asyncio
import json
import os
import sys

from .utils import psi, plgSelf, tr
from .utils.token import getToken
from .reporter import sendMsg
from mcdreforged.api.decorator import new_thread
from nio import AsyncClient, LoginResponse


clientStatus = False

# Cache Token.
def cache_token(resp: LoginResponse):
    from .config import TOKEN_FILE, user_id
    with open(TOKEN_FILE, "w") as f:
        json.dump(
            {
                "user_id": user_id,
                "token": resp.access_token
            },
            f,
        )

# Init Matrix bot.
@new_thread('MatrixInitClient')
def init():
    asyncio.run(init_task())

async def init_task():
    await init_client()

async def init_client() -> None:
    from .config import TOKEN_FILE, homeserver, user_id, password, device_id
    if not os.path.exists(TOKEN_FILE):
        psi.logger.info(tr("run_tips.first_time_login"))
        client = AsyncClient(homeserver, user_id)
        resp = await client.login(password, device_name=f"{device_id}")
        if isinstance(resp, LoginResponse):
            psi.logger.info(tr("run_tips.login_success"))
            cache_token(resp)
            psi.logger.info(tr("run_tips.get_token"))
            await test_client()
        else:
            failed_tip = tr("run_tips.failed")
            homeserver_tr = tr("tr.hs")
            account_tr = tr("tr.ac")
            psi.logger.info(f"{failed_tip}: {resp}")
            psi.logger.info(f'{homeserver_tr}: "{homeserver}", {account_tr}: "{user_id}"')
            psi.logger.info(tr("run_tips.error"))
            sys.exit(1)
    else:
        user, token = await getToken()
        if user != user_id:
            psi.logger.error(tr("init_tips.user_mismatch"))
            psi.logger.info(tr("init_tips.do_unload"))
            psi.unload_plugin(plgSelf.id)
        else:
            await test_client()

# Send test messages.
async def test_client():
    global clientStatus
    message = tr("sync_tips.reporter_status")
    await sendMsg(message)
    clientStatus = True
