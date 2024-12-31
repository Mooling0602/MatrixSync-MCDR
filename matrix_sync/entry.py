import os

from .utils import tr
from .client.reporter import send_to_matrix
from .client.receiver import stop_sync
from .config import load_config
from .commands import *
from .event.receiver import listen_message
from mcdreforged.api.all import *


# Framwork ver: 2.5.1-2
async def on_load(server: PluginServerInterface, prev_module):
    await load_config(server)
    # await check_settings(server)
    command_register(server)
    if not os.path.exists(f"{configDir}/token.json"):
        from .client.init import login_by_password
        await login_by_password()
    listen_message(server)
    start_sync()

def on_server_start(server: PluginServerInterface):
    matrix_reporter(tr("server_status.starting"))

def on_server_startup(server: PluginServerInterface):
    start_sync()
    matrix_reporter(tr("server_status.on_startup"))

# Built-in game message reporter.
def on_user_info(server: PluginServerInterface, info: Info):
    if info.player is not None and not info.content.startswith("!!"):
        player_message = f"[MC] <{info.player}> {info.content}"
        if plg_globals.sync:
            matrix_reporter(player_message)

# Send a message about the status of server to matrix when server stop.
async def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        exit_message = tr("server_status.on_stop")
    else:
        exit_message = tr("server_status.on_crash")
    
    await send_to_matrix(exit_message)

# Wait for receiver sync exited, then unload plugin.
async def on_unload(server: PluginServerInterface):
    logger = get_logger()
    logger.info(tr("on_unload"))
    await stop_sync()