import asyncio
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter
from matrix_sync.client import init_client
from matrix_sync.receiver import getMsg
from matrix_sync.reporter import formater, sendMsg
from mcdreforged.api.all import *

psi = ServerInterface.psi()

# Default config.
account_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org",
    "room_name": "your-room-display-name"
}

# Bot manage config.
bot_config = {
    "plugin_enabled": False,
    "allow_all_rooms_msg": False,
    "use_token": True
}

def on_load(server: PluginServerInterface, old):
    global config, settings, DATA_FOLDR, TOKEN_FILE, homeserver
    config = server.load_config_simple("config.json", account_config)
    settings = server.load_config_simple("settings.json", bot_config)
    DATA_FOLDER = server.get_data_folder()
    tip_path = server.rtr("matrix_sync.init_tips.config_path")
    server.logger.info(f"{tip_path}: {DATA_FOLDER}")
    TOKEN_FILE = f"{DATA_FOLDER}/token.json"
    homeserver = config["homeserver"]
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + config["homeserver"]
    check_config()

# Check the config.
def check_config():
    if not settings["plugin_enabled"]:
        psi.logger.info(psi.rtr("matrix_sync.init_tips.need_edit_config"))
        psi.unload_plugin("matrix_sync")
    else:
        psi.logger.info(psi.rtr("matrix_sync.init_tips.read_config"))

# Sync processes.
@new_thread
def on_server_startup(server: PluginServerInterface):
    asyncio.run(init_client())
    if matrix_sync.client.clientStatus:
        asyncio.run(getMsg())

def on_user_info(server: PluginServerInterface, info: Info):
    formater(server, info)
    if matrix_sync.reporter.report:
        asyncio.run(sendMsg(matrix_sync.reporter.gameMsg))

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_server_stop"))

