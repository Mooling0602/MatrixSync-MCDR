# Codes sub thread MatrixReceiver running.
import asyncio
import matrix_sync.config

from matrix_sync.token import getToken
from mcdreforged.api.all import *
from nio import AsyncClient, MatrixRoom, RoomMessageText, SyncResponse, SyncError
from typing import Optional

psi = ServerInterface.psi()
client = None

class RoomMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room: Optional[str] = None):
        super().__init__('MatrixRoomMessage')  # 使用固定的事件ID
        self.message = message
        self.sender = sender
        self.room = room

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    user_id = matrix_sync.config.user_id
    room_name = matrix_sync.config.room_name
    roomMsg = f"[MSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
    transfer = True
    # Avoid echo messages.
    if event.sender == user_id:
        transfer = False
    # Apply settings config
    if not matrix_sync.config.settings["allow_all_rooms_msg"]:
        roomMsg = f"[MSync] {room.user_name(event.sender)}: {event.body}"
        if not room.display_name == room_name:
            transfer = False
        else:
            psi.dispatch_event(RoomMessageEvent(event.body, room.user_name(event.sender)), (event.body, room.user_name(event.sender)))
    else:
        psi.dispatch_event(RoomMessageEvent(event.body, room.user_name(event.sender), room.display_name), (event.body, room.user_name(event.sender), room.display_name))
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
    homeserver = matrix_sync.config.homeserver
    device_id = matrix_sync.config.device_id
    user_id = matrix_sync.config.user_id
    global client
    client = AsyncClient(f"{homeserver}")
    client.access_token = await getToken()
    client.user_id = user_id
    client.device_id = device_id

    client.add_response_callback(on_sync_response, SyncResponse)
    client.add_response_callback(on_sync_error, SyncError)
    client.add_event_callback(message_callback, RoomMessageText)
    
    try:
        await client.sync_forever(timeout=5)
    except asyncio.CancelledError:
        await client.close()
    finally:
        await client.close()
