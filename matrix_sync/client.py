import aiofiles
import asyncio
import json
import os
import sys
import matrix_sync.config
from matrix_sync.reporter import sendMsg
from mcdreforged.api.all import *
from nio import AsyncClient, LoginResponse

psi = ServerInterface.psi()
clientStatus = False

# Cache Token
def cache_token(resp: LoginResponse):
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    with open(TOKEN_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )

# Init Matrix bot
async def init_client() -> None:
    homeserver = matrix_sync.config.homeserver
    user_id = matrix_sync.config.user_id
    password = matrix_sync.config.password
    room_id = matrix_sync.config.room_id
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    device_id = matrix_sync.config.device_id
    psi.logger.info(user_id)
    if not os.path.exists(TOKEN_FILE):
        psi.logger.info(psi.rtr("matrix_sync.run_tips.first_time_login"))
        
        client = AsyncClient(homeserver, user_id)
        resp = await client.login(password, device_name=f"{device_id}")
        
        if isinstance(resp, LoginResponse):
            psi.logger.info(psi.rtr("matrix_sync.run_tips.login_success"))
            cache_token(resp)
            psi.logger.info(psi.rtr("matrix_sync.run_tips.get_token"))

            await test_client()
        else:
            failed_tip = psi.rtr("matrix_sync.run_tips.failed")
            homeserver_tr = psi.rtr("matrix_sync.tr.hs")
            account_tr = psi.rtr("matrix_sync.tr.ac")
            psi.logger.info(f"{failed_tip}: {resp}")
            psi.logger.info(f'{homeserver_tr}: "{homeserver}", {account_tr}: "{user_id}"')
            psi.logger.info(psi.rtr("matrix_sync.run_tips.error"))
            sys.exit(1)

    else:
        await test_client()

# Send test messages.
async def test_client():
    message = psi.rtr("matrix_sync.sync_tips.reporter_status")
    await sendMsg(message)
    global clientStatus
    clientStatus = True
