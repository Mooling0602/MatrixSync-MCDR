import asyncio
import multiprocessing
import matrix_sync.config
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter

from matrix_sync.client import init_client
from matrix_sync.config import load_config, check_config
from matrix_sync.receiver import getMsg
from matrix_sync.reporter import formater, sendMsg
from mcdreforged.api.all import *

psi = ServerInterface.psi()
lock = multiprocessing.Lock()
sync_task = None

def on_load(server: PluginServerInterface, old):
    load_config()
    server.logger.info(matrix_sync.config.load_tip)
    check_config()
    server.register_command(
        Literal('!!msync')
        .runs(
            lambda src: src.reply(manualSync())
        )
    )
    server.logger.info(psi.rtr("matrix_sync.init_tips.hotload_tip"))

def manualSync():
    if lock.acquire(block=False):
        asyncio.run(start_room_msg())
        return psi.rtr("matrix_sync.manual_sync.start_sync")
    else:
        return psi.rtr("matrix_sync.manual_sync.error")
                
# Sync processes.
@new_thread
def on_server_startup(server: PluginServerInterface):
    if lock.acquire(block=False):
        asyncio.run(init_client())
        clientStatus = matrix_sync.client.clientStatus
        if clientStatus:
            asyncio.run(start_room_msg())
    else:
        server.logger.info(server.rtr("matrix_sync.manual_sync.error"))

async def start_room_msg():
    await on_room_msg()

async def on_room_msg():
    global sync_task
    if sync_task is not None and not sync_task.done():
        sync_task.cancel()
        await sync_task
    sync_task = asyncio.create_task(getMsg())
    await sync_task

def on_user_info(server: PluginServerInterface, info: Info):
    formater(server, info)
    report = matrix_sync.reporter.report
    if report:
        gameMsg = matrix_sync.reporter.gameMsg
        asyncio.run(sendMsg(gameMsg))

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_server_stop"))

def on_unload(server: PluginServerInterface):
    global sync_task
    server.logger.info(server.rtr("matrix_sync.on_unload"))
    try:
        if sync_task is not None and not sync_task.done():
            sync_task.cancel()
    except Exception:
        pass
    finally:
        sync_task = None
        lock.release()