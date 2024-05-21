import aiofiles
import json
import re
import matrix_sync.client
import matrix_sync.entry
from mcdreforged.api.all import *
from nio import AsyncClient

psi = ServerInterface.psi()

def formater(server: PluginServerInterface, info: Info):
    # psi.logger.info(psi.rtr("matrix_sync.sync_tips.test"))
    # Debug code: Uncomment the above to determine whether game messages have been started to be reported.
    global message, report
    console_tr = psi.rtr("matrix_sync.tr.cs")
    message = f"<{info.player}> {info.content}"
    if info.player is None:
        if re.fullmatch(r'say \S*', info.content):
            msg_content = '{}'.format(info.content.rsplit(' ', 1)[1])
            message = f"<{console_tr}> {msg_content}"
        else:
            option = psi.rtr("matrix_sync.on_console.commands")
            message = f"<{console_tr}> {option} -> {info.content}"
        if info.content == "stop":
            message = psi.rtr("matrix_sync.sync_tips.server_stopping")
    report = False
    if matrix_sync.client.clientStatus:
        report = True

# Game Message reporter.
async def sendMsg() -> None:
    async with aiofiles.open(matrix_sync.entry.TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{matrix_sync.entry.homeserver}")
    client.access_token = cache["token"]
    client.user_id = matrix_sync.entry.config["user_id"]
    client.device_id = "mcdr"
    room_id = matrix_sync.entry.config["room_id"]

    await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
    )

    await client.close()