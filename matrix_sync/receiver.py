# thread MatrixReceiver
import asyncio
import matrix_sync.config

from .utils.token import getToken
from .utils import psi, plgSelf, tr
from mcdreforged.api.event import PluginEvent
from nio import AsyncClient, MatrixRoom, RoomMessageText, SyncError, RoomMessagesResponse
from typing import Optional


homeserver_online = True

def load_msg_filter(room_id: str):
    msg_filter = {"room_id": room_id}
    return msg_filter

class RoomMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room: Optional[str] = None):
        super().__init__('MatrixRoomMessage')  # 使用固定的事件ID
        self.message = message
        self.sender = sender
        self.room = room

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    transfer = False
    from .config import user_id, settings
    msg_format = settings["room_msg_format"]["multi_room"]
    roomMsg = msg_format.replace('%room_display_name%', room.display_name).replace('%sender%', room.user_name(event.sender)).replace('%message%', event.body)
    # Avoid echo messages.
    if not event.sender == user_id:
        # Apply settings config
        if not settings["allow_all_rooms_msg"]:
            msg_format = settings["room_msg_format"]["single_room"]
            roomMsg = msg_format.replace('%sender%', room.user_name(event.sender)).replace('%message%', event.body)
            # if response.room_id == room_id:
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
    from .config import homeserver, device_id, user_id, sync_old_msg, allow_all_rooms_msg
    from .config import room_id as cfg_room_id
    client = AsyncClient(f"{homeserver}")
    user, token = await getToken()
    client.access_token = token
    if user != user_id:
        if user is not None:
            tip = tr("init_tips.user_mismatch")
            psi.logger.error(tip.replace("%user_id%", user_id))
            psi.logger.info(tr("init_tips.do_unload"))
            psi.unload_plugin(plgSelf.id)
        else:
            psi.logger.error(tr("init_tips.token_invaild"))
            psi.logger.info(tr("init_tips.do_unload"))
            psi.unload_plugin(plgSelf.id)
    else:
        client.user_id = user_id
        client.device_id = device_id

    if not allow_all_rooms_msg:
        print("ok.")
        await client.upload_filter(room={"rooms": [cfg_room_id]})
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
            psi.logger.info("Use §7!!msync start §rafter homeserver is running or your network restored.")
    except Exception as e:
        psi.logger.error(f"Sync error: {e}")
    except asyncio.CancelledError:
        await client.close()
    finally:
        await client.close()
