import asyncio
import time
import matrix_sync.config
import matrix_sync.client
import matrix_sync.receiver
import matrix_sync.reporter
from matrix_sync.client import init_client
from matrix_sync.config import load_config, check_config
from matrix_sync.exit import unload
from matrix_sync.receiver import getMsg
from matrix_sync.reporter import formater, sendMsg
from mcdreforged.api.all import *

psi = ServerInterface.psi()
lockClient = False
ban_msync = False
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
    global lockClient
    if not ban_msync:
        asyncio.run(on_room_msg())
        lockClient = True
        return psi.rtr("matrix_sync.manual_sync.start_sync")
    else:
        return psi.rtr("matrix_sync.manual_sync.error")

# Sync processes.
@new_thread
def on_server_startup(server: PluginServerInterface):
    global ban_msync
    asyncio.run(init_client())
    if matrix_sync.client.clientStatus and not lockClient:
        ban_msync = True
        asyncio.run(start_room_msg())

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
    if matrix_sync.reporter.report:
        gameMsg = matrix_sync.reporter.gameMsg
        asyncio.run(sendMsg(gameMsg))

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        server.logger.info(server.rtr("matrix_sync.on_server_stop"))

def on_unload(server: PluginServerInterface):
    global sync_task
    unload()
    server.logger.info(server.rtr("matrix_sync.on_unload"))
    time.sleep(3)
    try:
        if sync_task is not None and not sync_task.done():
            sync_task.cancel()
    except Exception as e:
        server.logger.error(f"Error during canceling sync task: {e}")
    finally:
        sync_task = None