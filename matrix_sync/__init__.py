# Import needed APIs.
import asyncio
import json
import os
import sys
import aiofiles
import re

from mcdreforged.api.all import *
from nio import AsyncClient, LoginResponse, MatrixRoom, RoomMessageText

psi = ServerInterface.psi()

# Default config.
default_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org",
    "room_name": "your-room-display-name",
    "allow_all_rooms_msg": False,
    "user_name": "bot-display-name"
}

# Load plugin and init default config.
def on_load(server: PluginServerInterface, old):
    global config, DATA_FOLDR, TOKEN_FILE, homeserver

    config = server.load_config_simple("config.json", default_config)
    DATA_FOLDER = server.get_data_folder()
    CONFIG_PATH = server.rtr("matrix_sync.init_tips.config_path")
    server.logger.info(f"{CONFIG_PATH}: {DATA_FOLDER}")
    TOKEN_FILE = f"{DATA_FOLDER}/token.json"
    homeserver = config["homeserver"]
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + config["homeserver"]

    check_config()

# Check the config.
def check_config():
    if config["homeserver"] == "https://matrix.example.org" or config["user_id"] == "@username:matrix.example.org" or config["password"] == "your_password" or config["room_id"] == "!your-room_id:matrix.example.org" or config["user_name"] == "bot-display-name":
        psi.logger.info(psi.rtr("matrix_sync.init_tips.need_change_config"))
        psi.unload_plugin("matrix_sync")
    else:
        psi.logger.info(psi.rtr("matrix_sync.init_tips.read_config"))

# Cache Token.
def cache_token(resp: LoginResponse):
    with open(TOKEN_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )
    
# Init Matrix bot.
async def init_client() -> None:
    if not os.path.exists(TOKEN_FILE):
        psi.logger.info(psi.rtr("matrix_sync.run_tips.first_time_login"))
        user_id = config["user_id"]
        password = config["password"]
        
        client = AsyncClient(homeserver, user_id)
        resp = await client.login(password, device_name="matrix-nio")
        
        if isinstance(resp, LoginResponse):
            psi.logger.info(psi.rtr("matrix_sync.run_tips.login_success"))
            cache_token(resp)
            psi.logger.info(psi.rtr("matrix_sync.run_tips.get_token"))
        else:
            failed_tip = psi.rtr("matrix_sync.run_tips.failed")
            homeserver_tr = psi.rtr("matrix_sync.tr.hs")
            account_tr = psi.rtr("matrix_sync.tr.ac")
            psi.logger.info(f"{failed_tip}: {resp}")
            psi.logger.info(f'{homeserver_tr}: "{homeserver}", {account_tr}: "{user_id}"')
            psi.logger.info(psi.rtr("matrix_sync.run_tips.error"))
            sys.exit(1)

    else:
        async with aiofiles.open(TOKEN_FILE, "r") as f:
            contents = await f.read()
        cache = json.loads(contents)
        client = AsyncClient(f"{homeserver}")
        client.access_token = cache["token"]
        client.user_id = config["user_id"]
        client.device_id = "matrix-nio"
        room_id = config["room_id"]

        message = psi.rtr("matrix_sync.sync_tips.server_started")
        
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )
        
        global test_status
        test_status = True
        if test_status:
            psi.logger.info(psi.rtr("matrix_sync.sync_tips.start_report"))
    await client.close()


# Check connection and login, then feedback status.
@new_thread
def on_server_startup(server: PluginServerInterface):
    asyncio.run(init_client())
    if test_status:
        asyncio.run(get_msg())

        
def on_user_info(server: PluginServerInterface, info: Info):
    # psi.logger.info(psi.rtr("matrix_sync.sync_tips.test"))
    # Debug code: Uncomment the above to determine whether game messages have been started to be reported.
    global message
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
    flag = False
    if test_status:
        flag = True
    if flag:
        asyncio.run(send_msg())

# Game Message reporter.
async def send_msg() -> None:
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = config["user_id"]
    client.device_id = "matrix-nio"
    room_id = config["room_id"]

    await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
    )

    await client.close()

# Matrix Room Message receiver.
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    room_msg = f"[MatrixSync] {room.user_name(event.sender)}: {event.body}"
    transfer = True
    if not room.display_name == config["room_name"]:
        if config["allow_all_rooms_msg"]:
            room_msg = f"[MatrixSync|{room.display_name}] {room.user_name(event.sender)}: {event.body}"
        else:
            transfer = False
    if not room.user_name(event.sender) == config["user_name"]:
        if transfer:
            psi.broadcast(f"{room_msg}")

async def get_msg() -> None:
    async with aiofiles.open(TOKEN_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = config["user_id"]
    client.device_id = "matrix-nio"
    room_id = config["room_id"]

    client.add_event_callback(message_callback, RoomMessageText)
    await client.sync_forever(timeout=0)

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_stop"))
