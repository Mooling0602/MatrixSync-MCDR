import asyncio
import matrix_sync.config
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter

from matrix_sync.client import init_client
from matrix_sync.config import load_config, check_config
from matrix_sync.receiver import getMsg
from matrix_sync.reporter import formater, sendMsg
from mcdreforged.api.all import *

# Framwork ver: 2.2.0-stable
psi = ServerInterface.psi()
lock = asyncio.Lock()
cleaned = False
sync_task = None
asyncio_loop = None

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
                lambda src: src.reply(manualSync())
            )
        )
        server.logger.info(psi.rtr("matrix_sync.init_tips.hotload_tip"))

# Manually run sync processes.
@new_thread
def manualSync():
    if not lock.locked():
        asyncio.run(start_room_msg())
    else:
        return psi.rtr("matrix_sync.manual_sync.error")

# Automatically run sync processes.
@new_thread
def on_server_startup(server: PluginServerInterface):
    clientStatus = matrix_sync.client.clientStatus
    if not lock.locked():
        if clientStatus:
            message = psi.rtr("matrix_sync.sync_tips.server_started")
            asyncio.run(sendMsg(message))
            asyncio.run(start_room_msg())
    else:
        server.logger.info(server.rtr("matrix_sync.manual_sync.error"))

async def start_room_msg():
    async with lock:
        await on_room_msg()

async def on_room_msg():
    global sync_task
    if sync_task is not None and not sync_task.done():
        sync_task.cancel()
        await sync_task
    sync_task = asyncio.create_task(getMsg())
    await sync_task

# Game message reporter
def on_user_info(server: PluginServerInterface, info: Info):
    formater(server, info)
    report = matrix_sync.reporter.report
    if report:
        gameMsg = matrix_sync.reporter.gameMsg
        asyncio.run(sendMsg(gameMsg))

# Exit sync process.
def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global cleaned
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_server_stop"))
    else:
        server.logger.info(server.rtr("matrix_sync.on_server_crash"))
        crashTip = server.rtr("matrix_sync.sync_tips.server_crashed")
        clientStatus = matrix_sync.client.clientStatus
        if clientStatus:
            asyncio.run(sendMsg(crashTip))
        
    if sync_task is not None:
        sync_task.cancel()
        try:
            asyncio.wait_for(sync_task, timeout=5)
        except asyncio.TimeoutError:
            server.logger.warning("Timed out waiting for sync_task to finish.")
        except asyncio.CancelledError:
            pass
    
    cleaned = True

def on_unload(server: PluginServerInterface):
    global sync_task, cleaned
    if cleaned:
        server.logger.info(server.rtr("matrix_sync.on_unload"))
    else:
        if sync_task is not None:
            sync_task.cancel()
            try:
                asyncio.wait_for(sync_task, timeout=5)
            except asyncio.TimeoutError:
               server.logger.warning("Timed out waiting for sync_task to finish.")
            except asyncio.CancelledError:
                pass
        sync_task = None
        lock_is_None = matrix_sync.config.lock_is_None
        if not lock_is_None:
            server.logger.info(server.rtr("matrix_sync.on_unload"))
