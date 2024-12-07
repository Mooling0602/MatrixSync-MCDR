import asyncio
from . import tr

from mcdreforged.api.all import *
from .globals import *
from ..receiver import getMsg

sync_task = None

def plugin_command(server: PluginServerInterface):
    server.register_help_message("!!msync", help())
    server.register_command(
        Literal('!!msync')
        .then(
            Literal('start')
            .runs(
                lambda src: src.reply(manualSync())
            )
        )
        .then(
            Literal('stop')
            .runs(
                lambda src: src.reply(stopSync(src))
            )
        )
    )

# Help tips.
def help() -> RTextList:
    return RTextList(
        psi.rtr(f"{plgSelf.id}.help_tips.title") + "\n",
        psi.rtr(f"{plgSelf.id}.help_tips.start_command") + "\n",
        psi.rtr(f"{plgSelf.id}.help_tips.stop_command") + "\n",
        psi.rtr(f"{plgSelf.id}.help_tips.closetip_command") + "\n"
    )

# Manually run sync processes.
def manualSync():
    if not tLock.locked():
        start_room_msg()
        return tr("manual_sync.start_sync")
    else:
        return tr("manual_sync.start_error")

def exit_sync():
    global sync_task
    try:
        if sync_task is not None:
            sync_task.cancel()
            sync_task = None
            return tr("manual_sync.stop_sync")
        else:
            return tr("manual_sync.not_running")
    except Exception:
        return tr("manual_sync.stop_error")
    

# Manually stop sync processes.
def stopSync(src):
    if src.is_console:
        return exit_sync()
    else:
        return tr("manual_sync.stop_denied")

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