import aiofiles
import json
import re
import os
import matrix_sync.client
import matrix_sync.config
from mcdreforged.api.all import *
from nio import AsyncClient

psi = ServerInterface.psi()

def formater(server: PluginServerInterface, info: Info):
    # psi.logger.info(psi.rtr("matrix_sync.sync_tips.test"))
    # Debug code: Uncomment the above to determine whether game messages have been started to be reported.
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    global gameMsg, report
    console_tr = psi.rtr("matrix_sync.tr.cs")
    gameMsg = f"<{info.player}> {info.content}"
    if info.player is None:
        if re.fullmatch(r'say \S*', info.content):
            msg_content = '{}'.format(info.content.rsplit(' ', 1)[1])
            gameMsg = f"<{console_tr}> {msg_content}"
        else:
            option = psi.rtr("matrix_sync.on_console.commands")
            gameMsg = f"* {console_tr} {option} -> {info.content}"
        if info.content == "stop":
            gameMsg = psi.rtr("matrix_sync.sync_tips.server_stopping")
    else:
        if info.content.startswith("!!"):
            option = psi.rtr("matrix_sync.on_console.commands")
            gameMsg = f"* {info.player} {option} -> {info.content}"
    report = False
    if os.path.exists(TOKEN_FILE):
        report = True

# Game Message reporter.
async def sendMsg(message) -> None:
    homeserver = matrix_sync.config.homeserver
    user_id = matrix_sync.config.user_id
    room_id = matrix_sync.config.room_id
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    device_id = matrix_sync.config.device_id
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
