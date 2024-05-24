import asyncio
import aiofiles
import json
import matrix_sync.entry
from mcdreforged.api.all import *
from nio import AsyncClient, MatrixRoom, RoomMessageText

psi = ServerInterface.psi()

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    roomMsg = f"[MatrixSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
    # 启用消息响应 API 的前置条件，非指定房间的消息无法触发
    if room.display_name == matrix_sync.entry.config["room_name"]:
        reactor = True
    else:
        reactor = False
    transfer = True
    if not matrix_sync.entry.settings["allow_all_rooms_msg"]:
        roomMsg = f"[MatrixSync] {room.user_name(event.sender)}: {event.body}"
        if not room.display_name == matrix_sync.entry.config["room_name"]:
            transfer = False
    if event.sender == matrix_sync.entry.config["user_id"]:
        transfer = False
    if transfer:
        psi.broadcast(f"{roomMsg}")

async def getMsg() -> None:
    async with aiofiles.open(matrix_sync.entry.TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{matrix_sync.entry.homeserver}")
    client.access_token = cache["token"]
    client.user_id = matrix_sync.entry.config["user_id"]
    client.device_id = "mcdr"
    room_id = matrix_sync.entry.config["room_id"]

    client.add_event_callback(message_callback, RoomMessageText)
    await client.sync_forever(timeout=10)