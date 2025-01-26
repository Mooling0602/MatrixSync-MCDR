# thread MatrixReceiver
import asyncio
import matrix_sync.plg_globals as plg_globals

from . import *
from ..utils.token import getToken
from ..utils.get_logger import console_logger
from mutils import tr
from ..event import *
from nio import MatrixRoom, RoomMessageText, SyncError, UploadFilterError


homeserver_online = True

receiver = None

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    room_info.id = room.room_id
    room_info.display_name= room.display_name
    if event.sender != plg_globals.config["user_id"]:
        event_dispatcher(MatrixMessageEvent, event.body, room.user_name(event.sender), room_info)

def on_sync_error(response: SyncError):
    logger = console_logger()
    global homeserver_online
    logger.error(f"Sync error: {response.status_code}", "Receiver")
    if response.status_code >= 500:
        homeserver_online = False

async def get_messages() -> None:
    logger = console_logger()
    global receiver
    resp = None
    client = AsyncClient(homeserver=get_homeserver(plg_globals.config["homeserver"]))

    client.user_id = plg_globals.config["user_id"]
    user, token = await getToken()
    client.access_token = token
    client.device_id = plg_globals.config["device_id"]

    if not plg_globals.settings["listen"]["all_rooms"]:
        logger.info("ok.", "Receiver")
        cfg_room_id = plg_globals.config["room_id"]
        logger.info(f"Listening: {cfg_room_id}", "Receiver")
        resp = await client.upload_filter(room={"rooms": [cfg_room_id]})
        if isinstance(resp, UploadFilterError):
            logger.error(resp, "Receiver")

    client.add_response_callback(on_sync_error, SyncError)
    
    if homeserver_online:
        if plg_globals.settings["listen"]["old_messages"] is True:
            receiver = asyncio.create_task(client.sync_forever(timeout=5))
        else:
            if resp is not None:
                await client.sync(timeout=5, sync_filter=resp.filter_id)
                client.add_event_callback(message_callback, RoomMessageText)
                receiver = asyncio.create_task(client.sync_forever(timeout=5, sync_filter=resp.filter_id))
            else:
                await client.sync(timeout=5)
                client.add_event_callback(message_callback, RoomMessageText)
                receiver = asyncio.create_task(client.sync_forever(timeout=5))
    else:
        logger.error("Sync failed: homeserver is down or your network disconnected with it.", "Receiver")
        logger.info("Use !!msync start after homeserver is running or your network restored.", "Receiver")
        
    try:
        await receiver
    except asyncio.CancelledError:
        logger.warning(tr("on_receiver_cancelled"), "Receiver")
    except Exception as e:
        logger.error(f"Receiver sync error: {e}", "Receiver")
        receiver.cancel()
    finally:
        if receiver:
            receiver.cancel()
        if client is not None:
            await client.close()

async def stop_sync():
    if isinstance(receiver, asyncio.Task):
        receiver.cancel()
        plg_globals.sync = False