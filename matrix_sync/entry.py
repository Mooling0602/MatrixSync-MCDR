import time

from typing import Optional
from .utils import tr
from .client import init, clientStatus
from .config import load_config, check_config
from .utils import psi, globals
from .utils.commands import *
from .reporter import send_matrix
from mcdreforged.api.all import *


# Framwork ver: 2.4.1
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
        if server.is_server_startup() and clientStatus:
            start_sync()

# Automatically run sync processes.
def start_sync(on_reload: Optional[bool] = True):
    if not globals.tLock.locked():
        start_room_msg()
        if not on_reload:
            time.sleep(1)
            message = tr("sync_tips.server_started")
            send_matrix(message)
    else:
        psi.logger.info(tr("manual_sync.start_error"))

def on_server_startup(server: PluginServerInterface):
    start_sync(False)

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

    # 鉴于有用户反馈关服时消息发送不到Matrix，这里卡一个协程用于发送
    # 为了防止卡住MCDR主线程出现无响应提示影响用户体验，一般都在子线程中发送消息，但是直接用协程正常情况下也没啥问题
    # 有bug的话应该会有人在issues提出，暂时先这么解决
    from .reporter import sendMsg
    asyncio.run(sendMsg(exit_message))
    
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
