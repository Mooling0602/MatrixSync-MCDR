# Import needed APIs.
import asyncio
import json
import re
import os
import sys
import aiofiles

from mcdreforged.api.all import *
from nio import AsyncClient, LoginResponse, MatrixRoom, RoomMessageText

psi = ServerInterface.psi()

# Default config.
default_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org",
    "user_name": "bot-display-name"
}

# Load plugin and init default config.
def on_load(server: PluginServerInterface, old):
    global config, DATA_FOLDER, DATA_FILE, homeserver

    config = server.load_config_simple("config.json", default_config)
    DATA_FOLDER = server.get_data_folder()
    server.logger.info(f"Config path: {DATA_FOLDER}")
    DATA_FILE = f"{DATA_FOLDER}/token.json"
    homeserver = config["homeserver"]
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + config["homeserver"]

    check_config(server)

# Check the config.
def check_config(server: PluginServerInterface):
    if config["homeserver"] == "https://matrix.example.org" or config["user_id"] == "@username:matrix.example.org" or config["password"] == "your_password" or config["room_id"] == "!your-room_id:matrix.example.org" or config["user_name"] == "bot-display-name":
        server.logger.info("Edit default config and reload plugin!")
        server.unload_plugin("matrix_sync")
    else:
        server.logger.info("Applying precent config, please wait...")

# Cache data.
def cache_data(resp: LoginResponse):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )
    
# Init Matrix bot.
async def init_client(server: PluginServerInterface) -> None:
    if not os.path.exists(DATA_FILE):
        server.logger.info("First login, continuing with password...")
        user_id = config["user_id"]
        password = config["password"]
        
        client = AsyncClient(homeserver, user_id)
        resp = await client.login(password, device_name="matrix-nio")
        
        if isinstance(resp, LoginResponse):
            server.logger.info("Login successfully, caching data for later use...")
            cache_data(resp)
            server.logger.info("Cache finished! ")
        else:
            server.logger.info(f"Bot login failed: {resp}")
            server.logger.info(f'Homeserver: "{homeserver}", Account: "{user_id}"')
            server.logger.info("Please check your account, password and network conditions, you can issue in GitHub for any help.")
            sys.exit(1)

    else:
        async with aiofiles.open(DATA_FILE, "r") as f:
            contents = await f.read()
        cache = json.loads(contents)
        client = AsyncClient(f"{homeserver}")
        client.access_token = cache["token"]
        client.user_id = config["user_id"]
        client.device_id = "matrix-nio"
        room_id = config["room_id"]

        message = "MC Server started successfully! "
        
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )
        
        global test_status
        test_status = True
        if test_status:
            server.logger.info("Bot login successfully, sent a test message.")
    await client.close()


# Check connection and login, feedback status.
@new_thread
def on_server_startup(server: PluginServerInterface):
    asyncio.run(init_client(server))
    if test_status:
        asyncio.run(get_msg())

        
def on_user_info(server: PluginServerInterface, info: Info):
        # server.logger.info("Player message detected, trying to send to Matrix group...")
        # Uncomment the above to determine whether game messages have started to be reported.
        global message
        message = f"<{info.player}> {info.content}"
        if info.player is None:
            message = f"<Console> {info.content}"
        flag = False
        if test_status:
            flag = True
        if flag:
            asyncio.run(send_msg(server))

# Message reporter.
async def send_msg(server: PluginServerInterface) -> None:
    async with aiofiles.open(DATA_FILE, "r") as f:
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

# i18n will be available in ver 1.1.0 and later.

# Message receiver.
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    room_msg = f"[MatrixSync] {room.user_name(event.sender)}: {event.body}"
    if not room.user_name(event.sender) == config["user_name"]:
        psi.broadcast(f"{room_msg}")

async def get_msg() -> None:
    async with aiofiles.open(DATA_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = config["user_id"]
    client.device_id = "matrix-nio"
    room_id = config["room_id"]

    client.add_event_callback(message_callback, RoomMessageText)
    await client.sync_forever(timeout=300000)

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code != 0:
        asyncio.close(get_msg())
