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


# Cache Token.
def cache_token(resp: LoginResponse):
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    with open(TOKEN_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )

# Init Matrix bot.
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
        resp = await client.login(password, device_name="mcdr1")
        
        if isinstance(resp, LoginResponse):
            psi.logger.info(psi.rtr("matrix_sync.run_tips.login_success"))
            cache_token(resp)
            psi.logger.info(psi.rtr("matrix_sync.run_tips.get_token"))
        else:
            failed_tip = psi.rtr("matrix_sync.run_tips.failed")
            homeserver_tr = psi.rtr("matrix_sync.tr.hs")
            account_tr = psi.rtr("matrix_sync.tr.ac")
            psi.logger.info(f"{failed_tip}: {resp}")
            psi.logger.info(f'{homeserver_tr}: "{homeserver}", {account_tr}: "{user_id}"')
            psi.logger.info(psi.rtr("matrix_sync.run_tips.error"))
            sys.exit(1)

    else:
        message = psi.rtr("matrix_sync.sync_tips.server_started")
        async with aiofiles.open(TOKEN_FILE, "r") as f:
            contents = await f.read()
        cache = json.loads(contents)
        client = AsyncClient(f"{homeserver}")
        client.access_token = cache["token"]
        client.user_id = user_id
        client.device_id = device_id

        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )

        await client.close()

        global clientStatus
        clientStatus = True
        if clientStatus:
            psi.logger.info(psi.rtr("matrix_sync.sync_tips.start_report"))