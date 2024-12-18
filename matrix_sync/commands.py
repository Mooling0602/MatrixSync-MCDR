import asyncio
import threading
import matrix_sync.globals as globals

from typing import Optional
from mcdreforged.api.all import *
from .client.reporter import send_to_matrix
from .client.receiver import get_messages, stop_sync
from .client import *
from .utils import tr
from .utils.logger import *

builder = SimpleCommandBuilder()

globals.tLock = threading.Lock()

def start_sync(on_reload: Optional[bool] = True):
    if not globals.tLock.locked():
        if not on_reload:
            matrix_reporter("MC server startup!")
        run_sync_task()
        log_info("Starting receiver sync...")
    else:
        log_warning("Already running receiver sync.")

@new_thread('MatrixReceiver')
def run_sync_task():
    globals.sync = True
    with globals.tLock:
        asyncio.run(add_sync_task())

async def add_sync_task():
    await get_messages()

@new_thread('MatrixReporter')
def matrix_reporter(message: str):
    asyncio.run(add_report_task(message))

async def add_report_task(message: str):
    report_task = asyncio.create_task(send_to_matrix(message))
    await report_task

def command_register(server: PluginServerInterface):
    builder.register(server)

@builder.command("!!msync start")
def on_command_start():
    start_sync()

@builder.command("!!msync stop")
async def on_command_stop():
    await stop_sync()

@builder.command("!!msync status")
def show_status():
    log_info(f"Receiver: {globals.sync}")