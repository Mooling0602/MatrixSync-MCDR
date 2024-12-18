import asyncio

from .utils import tr
from .utils.logger import *
from .client.reporter import send_to_matrix
from .client.receiver import stop_sync
from .config import load_config
from .commands import *
from mcdreforged.api.all import *


# Framwork ver: 2.5.0-1
def on_load(server: PluginServerInterface, prev_module):
    asyncio.run(load_config(server))
    command_register(server)
    start_sync()

def on_server_startup(server: PluginServerInterface):
    start_sync(False)

async def on_user_info(server: PluginServerInterface, info: Info):
    if info.player is not None and not info.content.startswith("!!"):
        playerMsg = f"[MC] <{info.player}> {info.content}"
        await send_to_matrix(playerMsg)

# Exit sync process when server stop.
async def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        log_info("Stop receiver sync due to server stopped.")
        exit_message = "MC Server stopped."
    else:
        log_warning("Exit receiver sync due to server crashed!")
        exit_message = "MC Server crashed!"

    await send_to_matrix(exit_message)

async def on_unload(server: PluginServerInterface):
    log_info("Unloading MatrixSync...")
    await stop_sync()