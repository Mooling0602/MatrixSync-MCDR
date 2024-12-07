from .utils.globals import *
from .utils import tr
from .client import init
from .config import load_config, check_config, load_tip, do_unload
from .utils.commands import *
from .reporter import send_matrix
from mcdreforged.api.all import *


# Framwork ver: 2.4.1-2
def on_load(server: PluginServerInterface, prev_module):
    load_config()
    server.logger.info(load_tip)
    check_config()
    if do_unload:
        server.unload_plugin(plgSelf.id)
    else:
        init()
        plugin_command(server)
        server.logger.info(tr("init_tips.hotload_tip"))
    
# Restart room message receiver, not recommend.
# def restartSync(src):
#     stopSync(src)
#     manualSync()

# Automatically run sync processes.
def on_server_startup(server: PluginServerInterface):
    from .client import clientStatus
    if not tLock.locked():
        if clientStatus:
            message = tr("sync_tips.server_started")
            send_matrix(message)
            start_room_msg()
    else:
        server.logger.info(tr("manual_sync.start_error"))

# Game message reporter
def on_user_info(server: PluginServerInterface, info: Info):
    # formater(server, info)
    if info.player is not None and not info.content.startswith("!!"):
        playerMsg = f"<{info.player}> {info.content}"
        from .client import clientStatus
        if clientStatus:
            send_matrix(playerMsg)

# Exit sync process when server stop.
def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global cleaned
    if server_return_code == 0:
        server.logger.info(tr("on_server_stop"))
        from .client import clientStatus
        stopTip = tr("sync_tips.server_stopped")
        if clientStatus:
            send_matrix(stopTip)
    else:
        server.logger.info(tr("on_server_crash"))
        crashTip = tr("sync_tips.server_crashed")
        from .client import clientStatus
        if clientStatus:
            send_matrix(crashTip)
        
    psi.logger.info(exit_sync())
    
    cleaned = True

def on_unload(server: PluginServerInterface):
    server.logger.info(tr("unload_tips.on_clean"))
    global cleaned, sync_stopped
    if cleaned:
        server.logger.info(tr("on_unload"))
    else:
        psi.logger.info(tr("unload_tips.start_clean"))
        psi.logger.info(exit_sync())
        if not lock_is_None:
            server.logger.info(tr("on_unload"))