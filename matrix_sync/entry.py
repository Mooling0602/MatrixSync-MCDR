import time

from .utils import tr
from .client import init
from .config import load_config, check_config
from .utils import psi, globals
from .utils.commands import *
from .reporter import send_matrix
from mcdreforged.api.all import *


# Framwork ver: 2.4.1-2
def on_load(server: PluginServerInterface, prev_module):
    load_config()
    from .config import load_tip
    server.logger.info(load_tip)
    check_config()
    from .config import do_unload
    if do_unload:
        server.unload_plugin(plgSelf.id)
    else:
        init()
        plugin_command(server)
        server.logger.info(tr("init_tips.hotload_tip"))

# Automatically run sync processes.
def on_server_startup(server: PluginServerInterface):
    if not globals.tLock.locked():
        message = tr("sync_tips.server_started")
        start_room_msg()
        time.sleep(1)
        send_matrix(message)
    else:
        server.logger.info(tr("manual_sync.start_error"))

# Game message reporter
def on_user_info(server: PluginServerInterface, info: Info):
    if info.player is not None and not info.content.startswith("!!"):
        playerMsg = f"<{info.player}> {info.content}"
        send_matrix(playerMsg)

# Exit sync process when server stop.
def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        server.logger.info(tr("on_server_stop"))
        exit_message = tr("sync_tips.server_stopped")
    else:
        server.logger.info(tr("on_server_crash"))
        exit_message = tr("sync_tips.server_crashed")

    send_matrix(exit_message)
    
    globals.cleaned = True

def on_unload(server: PluginServerInterface):
    server.logger.info(tr("unload_tips.on_clean"))
    if globals.cleaned:
        server.logger.info(tr("on_unload"))
    else:
        psi.logger.info(tr("unload_tips.start_clean"))
        psi.logger.info(exit_sync())
        from .config import lock_is_None
        if not lock_is_None:
            server.logger.info(tr("on_unload"))