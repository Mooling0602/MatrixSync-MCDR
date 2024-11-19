# thread MatrixReceiver
import asyncio
import matrix_sync.config

from matrix_sync.utils.token import getToken
from matrix_sync.utils.globals import psi
from mcdreforged.api.all import *
from nio import AsyncClient, MatrixRoom, RoomMessageText, SyncError
from typing import Optional

homeserver_online = True

class RoomMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room: Optional[str] = None):
        super().__init__('MatrixRoomMessage')  # 使用固定的事件ID
        self.message = message
        self.sender = sender
        self.room = room

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    transfer = False
    user_id = matrix_sync.config.user_id
    room_name = matrix_sync.config.room_name
    roomMsg = f"[MSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
    # Avoid echo messages.
    if not event.sender == user_id:
        # Apply settings config
        if not matrix_sync.config.settings["allow_all_rooms_msg"]:
            roomMsg = f"§7[MSync] §b{room.user_name(event.sender)} §6>>§r {event.body}"
            if room.display_name == room_name:
                transfer = True
                psi.dispatch_event(RoomMessageEvent(event.body, room.user_name(event.sender)), (event.body, room.user_name(event.sender)))
        else:
            psi.dispatch_event(RoomMessageEvent(event.body, room.user_name(event.sender), room.display_name), (event.body, room.user_name(event.sender), room.display_name))
        if transfer:
            psi.broadcast(f"{roomMsg}")

def on_sync_error(response: SyncError):
    global homeserver_online
    psi.logger.error(f"Sync error: {response.status_code}")
    if response.status_code >= 500:
        homeserver_online = False

async def getMsg() -> None:
    global next_batch, msg_callback
    homeserver = matrix_sync.config.homeserver
    device_id = matrix_sync.config.device_id
    user_id = matrix_sync.config.user_id
    sync_old_msg = matrix_sync.config.sync_old_msg
    client = AsyncClient(f"{homeserver}")
    client.access_token = await getToken()
    client.user_id = user_id
    client.device_id = device_id

    client.add_response_callback(on_sync_error, SyncError)
    
    try:
        if homeserver_online:
            if sync_old_msg is True:
                await client.sync_forever(timeout=5)
            else:
                await client.sync(timeout=5)
                client.add_event_callback(message_callback, RoomMessageText)
                await client.sync_forever(timeout=5)
        else:
            psi.logger.error("Sync failed: homeserver is down or your network disconnected with it.")
            psi.logger.info("Use !!msync start after homeserver is running or your network restored.")
    except Exception as e:
        psi.logger.error(f"Sync error: {e}")
    except asyncio.CancelledError:
        await client.close()
    finally:
        await client.close()
