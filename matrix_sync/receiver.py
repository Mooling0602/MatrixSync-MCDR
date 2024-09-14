import asyncio
import aiofiles
import json
import matrix_sync.config
from matrix_sync.reporter import sendMsg
from mcdreforged.api.all import *
from nio import AsyncClient, MatrixRoom, RoomMessageText, SyncResponse, SyncError

psi = ServerInterface.psi()

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    roomMsg = f"[MSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
    user_id = matrix_sync.config.user_id
    room_name = matrix_sync.config.room_name
    transfer = True
    if not matrix_sync.config.settings["allow_all_rooms_msg"]:
        roomMsg = f"[MSync] {room.user_name(event.sender)}: {event.body}"
        if not room.display_name == room_name:
            transfer = False
    if event.sender == user_id:
        transfer = False
    if transfer:
        psi.broadcast(f"{roomMsg}")

def on_sync_response(response: SyncResponse):
    global server_is_online
    server_is_online = True

def on_sync_error(response: SyncError):
    global server_is_online
    if response.status_code >= 500:
        server_is_online = False

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

    client.add_response_callback(on_sync_response, SyncResponse)
    client.add_response_callback(on_sync_error, SyncError)
    client.add_event_callback(message_callback, RoomMessageText)
    
    try:
        await client.sync_forever(timeout=5)
    except asyncio.CancelledError:
        await client.close()
