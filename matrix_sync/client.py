import aiofiles
import json
import os
import sys
import matrix_sync.entry
from mcdreforged.api.all import *
from nio import AsyncClient, LoginResponse

psi = ServerInterface.psi()

# Cache Token.
def cache_token(resp: LoginResponse):
    with open(matrix_sync.entry.TOKEN_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )

# Init Matrix bot.
async def init_client() -> None:
    if not os.path.exists(matrix_sync.entry.TOKEN_FILE) or not matrix_sync.entry.settings["use_token"]:
        psi.logger.info(psi.rtr("matrix_sync.run_tips.first_time_login"))
        user_id = matrix_sync.entry.config["user_id"]
        password = matrix_sync.entry.config["password"]
        
        client = AsyncClient(matrix_sync.entry.homeserver, user_id)
        resp = await client.login(password, device_name="matrix-nio")
        
        if isinstance(resp, LoginResponse):
            psi.logger.info(psi.rtr("matrix_sync.run_tips.login_success"))
            cache_token(resp)
            psi.logger.info(psi.rtr("matrix_sync.run_tips.get_token"))
        else:
            failed_tip = psi.rtr("matrix_sync.run_tips.failed")
            matrix_sync.entry.homeserver_tr = psi.rtr("matrix_sync.tr.hs")
            account_tr = psi.rtr("matrix_sync.tr.ac")
            psi.logger.info(f"{failed_tip}: {resp}")
            psi.logger.info(f'{matrix_sync.entry.homeserver_tr}: "{matrix_sync.entry.homeserver}", {account_tr}: "{user_id}"')
            psi.logger.info(psi.rtr("matrix_sync.run_tips.error"))
            sys.exit(1)

    else:
        async with aiofiles.open(matrix_sync.entry.TOKEN_FILE, "r") as f:
            contents = await f.read()
        cache = json.loads(contents)
        client = AsyncClient(f"{matrix_sync.entry.homeserver}")
        client.access_token = cache["token"]
        client.user_id = matrix_sync.entry.config["user_id"]
        client.device_id = "matrix-nio"
        room_id = matrix_sync.entry.config["room_id"]

        message = psi.rtr("matrix_sync.sync_tips.server_started")
        
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )
        
        global clientStatus
        clientStatus = True
        if clientStatus:
            psi.logger.info(psi.rtr("matrix_sync.sync_tips.start_report"))
    await client.close()