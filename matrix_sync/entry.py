import asyncio
import matrix_sync.config
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter

from matrix_sync.utils.globals import *
from matrix_sync.client import init
from matrix_sync.config import load_config, check_config
from matrix_sync.utils.commands import *
from matrix_sync.reporter import send_matrix
from mcdreforged.api.all import *

# Framwork ver: 2.4.0-3
def on_load(server: PluginServerInterface, prev_module):
    load_config()
    server.logger.info(matrix_sync.config.load_tip)
    check_config()
    do_unload = matrix_sync.config.do_unload
    if do_unload:
        server.unload_plugin("matrix_sync")
    else:
        init()
        plugin_command(server)
        server.logger.info(psi.tr("matrix_sync.init_tips.hotload_tip"))
    
# Restart room message receiver, not recommend.
# def restartSync(src):
#     stopSync(src)
#     manualSync()

# Automatically run sync processes.
def on_server_startup(server: PluginServerInterface):
    clientStatus = matrix_sync.client.clientStatus
    if not tLock.locked():
        if clientStatus:
            message = psi.tr("matrix_sync.sync_tips.server_started")
            send_matrix(message)
            start_room_msg()
    else:
        server.logger.info(server.tr("matrix_sync.manual_sync.start_error"))

# Game message reporter
def on_user_info(server: PluginServerInterface, info: Info):
    # formater(server, info)
    if info.player is not None and not info.content.startswith("!!"):
        playerMsg = f"<{info.player}> {info.content}"
        clientStatus = matrix_sync.client.clientStatus
        if clientStatus:
            send_matrix(playerMsg)

# Exit sync process when server stop.
def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global cleaned
    if server_return_code == 0:
        server.logger.info(server.tr("matrix_sync.on_server_stop"))
        clientStatus = matrix_sync.client.clientStatus
        stopTip = server.tr("matrix_sync.sync_tips.server_stopped")
        if clientStatus:
            send_matrix(stopTip)
    else:
        server.logger.info(server.tr("matrix_sync.on_server_crash"))
        crashTip = server.tr("matrix_sync.sync_tips.server_crashed")
        clientStatus = matrix_sync.client.clientStatus
        if clientStatus:
            send_matrix(crashTip)
        
    psi.logger.info(exit_sync())
    
    cleaned = True

def on_unload(server: PluginServerInterface):
    server.logger.info("执行清理进程")
    global cleaned, sync_stopped
    if cleaned:
        server.logger.info(server.tr("matrix_sync.on_unload"))
    else:
        psi.logger.info("正在准备清理...")
        psi.logger.info(exit_sync())
        if not lock_is_None:
            server.logger.info(server.tr("matrix_sync.on_unload"))