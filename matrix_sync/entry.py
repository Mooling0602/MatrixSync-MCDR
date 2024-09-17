import asyncio
import threading
import matrix_sync.config
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter

from matrix_sync.client import init_client
from matrix_sync.config import load_config, check_config
from matrix_sync.receiver import getMsg
from matrix_sync.reporter import gameMsgFormater, sendMsg
from mcdreforged.api.all import *

# Framwork ver: 2.3.0-1
psi = ServerInterface.psi()
tLock = threading.Lock()
lock_is_None = matrix_sync.config.lock_is_None
cleaned = False
sync_task = None

def on_load(server: PluginServerInterface, old):
    load_config()
    server.logger.info(matrix_sync.config.load_tip)
    check_config()
    do_unload = matrix_sync.config.do_unload
    if do_unload:
        server.unload_plugin("matrix_sync")
    else:
        asyncio.run(init_client())
        server.register_command(
            Literal('!!msync')
            .runs(
                lambda src: src.reply(help())
            )
            .then(
                Literal('start')
                .runs(
                    lambda src: src.reply(manualSync())
                )
            )
            .then(
                Literal('restart')
                .runs(
                    lambda src: src.reply(restartSync())
                )
            )
            .then(
                Literal('stop')
                .runs(
                    lambda src: src.reply(stopSync(src))
                )
            )
        )
        server.logger.info(psi.rtr("matrix_sync.init_tips.hotload_tip"))

# Help tips.
def help() -> RTextList:
    return RTextList(
        psi.rtr("matrix_sync.help_tips.title") + "\n",
        psi.rtr("matrix_sync.help_tips.start_command") + "\n",
        psi.rtr("matrix_sync.help_tips.stop_command") + "\n"
    )

# Manually run sync processes.
def manualSync():
    if not tLock.locked():
        start_room_msg()
        return psi.rtr("matrix_sync.manual_sync.start_sync")
    else:
        return psi.rtr("matrix_sync.manual_sync.start_error")

# Manually stop sync processes.
def stopSync(src):
    global sync_task
    if src.is_console:
        try:
            if sync_task is not None:
                sync_task.cancel()
                return psi.rtr("matrix_sync.manual_sync.stop_sync")
            else:
                return psi.rtr("matrix_sync.manual_sync.not_running")
        except Exception:
            return psi.rtr("matrix_sync.manual_sync.stop_error")
    else:
        return psi.rtr("matrix_sync.manual_sync.stop_denied")
    
# Restart room message receiver, not recommend
def restartSync():
    stopSync()
    manualSync()

# Automatically run sync processes.
def on_server_startup(server: PluginServerInterface):
    clientStatus = matrix_sync.client.clientStatus
    if not tLock.locked():
        if clientStatus:
            message = psi.rtr("matrix_sync.sync_tips.server_started")
            asyncio.run(sendMsg(message))
            start_room_msg()
    else:
        server.logger.info(server.rtr("matrix_sync.manual_sync.start_error"))

# Sub thread to receive room messages from matrix without block main MCDR thread.
@new_thread('MatrixReceiver')
def start_room_msg():
    with tLock:
        asyncio.run(on_room_msg())

async def on_room_msg():
    global sync_task
    if sync_task is not None and not sync_task.done():
        sync_task.cancel()
        await sync_task
    sync_task = asyncio.create_task(getMsg())
    await sync_task

# Game message reporter
def on_user_info(server: PluginServerInterface, info: Info):
    gameMsgFormater(server, info)
    report = matrix_sync.reporter.report
    if report:
        gameMsg = matrix_sync.reporter.gameMsg
        asyncio.run(sendMsg(gameMsg))

# Exit sync process when server stop.
def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global cleaned, sync_task
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_server_stop"))
        clientStatus = matrix_sync.client.clientStatus
        stopTip = server.rtr("matrix_sync.sync_tips.server_stopped")
        if clientStatus:
            asyncio.run(sendMsg(stopTip))
    else:
        server.logger.info(server.rtr("matrix_sync.on_server_crash"))
        crashTip = server.rtr("matrix_sync.sync_tips.server_crashed")
        clientStatus = matrix_sync.client.clientStatus
        if clientStatus:
            asyncio.run(sendMsg(crashTip))
        
    if sync_task is not None:
        sync_task.cancel()
        try:
            pass
        except asyncio.TimeoutError:
            server.logger.warning("Timed out waiting for sync_task to finish.")
    
    cleaned = True

def on_unload(server: PluginServerInterface):
    global sync_task, cleaned
    if cleaned:
        server.logger.info(server.rtr("matrix_sync.on_unload"))
    else:
        if sync_task is not None:
            sync_task.cancel()
            try:
                pass
            except asyncio.TimeoutError:
               server.logger.warning("Timed out waiting for sync_task to finish.")
        sync_task = None
        if not lock_is_None:
            server.logger.info(server.rtr("matrix_sync.on_unload"))
