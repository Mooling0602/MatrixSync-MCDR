import asyncio
import aiofiles
import json
import matrix_sync.config
from mcdreforged.api.all import *
from nio import AsyncClient, MatrixRoom, RoomMessageText

psi = ServerInterface.psi()

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    roomMsg = f"[MatrixSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
    user_id = matrix_sync.config.user_id
    room_name = matrix_sync.config.room_name
    transfer = True
    if not matrix_sync.config.settings["allow_all_rooms_msg"]:
        roomMsg = f"[MatrixSync] {room.user_name(event.sender)}: {event.body}"
        if not room.display_name == room_name:
            transfer = False
    if event.sender == user_id:
        transfer = False
    if transfer:
        psi.broadcast(f"{roomMsg}")

async def getMsg() -> None:
    user_id = matrix_sync.config.user_id
    homeserver = matrix_sync.config.homeserver
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    device_id = matrix_sync.config.device_id
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = user_id
    client.device_id = device_id

    client.add_event_callback(message_callback, RoomMessageText)
    
    try:
        await asyncio.wait_for(client.sync(), timeout=10)
        unloading = matrix_sync.exit.unloading
        if unloading:
            await client.close()
    except asyncio.TimeoutError as e:
        psi.logger.info(f"Sync task timed out: {e}")