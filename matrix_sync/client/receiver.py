# thread MatrixReceiver
import asyncio
import matrix_sync.globals as globals

from . import *
from .init import check_token
from ..utils.logger import *
from ..utils.token import getToken
from ..utils import tr
from ..event import *
from nio import MatrixRoom, RoomMessageText, SyncError, UploadFilterError


homeserver_online = True

receiver = None

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    message_format = globals.settings["message_format"]["all_room"]
    room_message = message_format.replace('%room_display_name%', room.display_name).replace('%sender%', room.user_name(event.sender)).replace('%message%', event.body)
    # Avoid echo messages.
    if not event.sender == globals.config["user_id"]:
        # Apply settings config
        if not globals.settings["sync"]["all_rooms"]:
            message_format = globals.settings["message_format"]["single_room"]
            room_message = message_format.replace('%sender%', room.user_name(event.sender)).replace('%message%', event.body)
        event_dispatcher(MatrixMessageEvent, event.body, room.user_name(event.sender), room.display_name)
        log_info(room_message, "Message")
        psi.say(room_message)

def on_sync_error(response: SyncError):
    global homeserver_online
    log_error(f"Sync error: {response.status_code}")
    if response.status_code >= 500:
        homeserver_online = False

async def get_messages() -> None:
    global receiver
    client = AsyncClient(homeserver=get_homeserver(globals.config["homeserver"]))
    token_vaild = await check_token()
    if token_vaild:
        user, token = await getToken()

        client.user_id = globals.config["user_id"]
        client.access_token = token
        client.device_id = globals.config["device_id"]

        if not globals.settings["sync"]["all_rooms"]:
            log_info("ok.")
            cfg_room_id = globals.config["room_id"]
            log_info(cfg_room_id)
            resp = await client.upload_filter(room={"rooms": [cfg_room_id]})
            if isinstance(resp, UploadFilterError):
                log_error(resp)

        client.add_response_callback(on_sync_error, SyncError)
    
        if homeserver_online:
            if globals.settings["sync"]["old_messages"] is True:
                receiver = asyncio.create_task(client.sync_forever(timeout=5, sync_filter=resp.filter_id))
            else:
                await client.sync(timeout=5, sync_filter=resp.filter_id)
                client.add_event_callback(message_callback, RoomMessageText)
                receiver = asyncio.create_task(client.sync_forever(timeout=5, sync_filter=resp.filter_id))
        else:
            log_error("Sync failed: homeserver is down or your network disconnected with it.")
            log_info("Use !!msync start after homeserver is running or your network restored.")
        
        try:
            await receiver
        except asyncio.CancelledError:
            log_warning("Receiver task was cancelled.")
        except Exception as e:
            log_error(f"Receiver sync error: {e}")
            receiver.cancel()
        finally:
            if receiver:
                receiver.cancel()
                try:
                    await receiver
                except asyncio.CancelledError:
                    pass
            client.stop_sync_forever()
            await client.close()

async def stop_sync():
    if isinstance(receiver, asyncio.Task):
        receiver.cancel()