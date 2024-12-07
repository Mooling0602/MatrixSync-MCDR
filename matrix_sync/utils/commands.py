import asyncio

from . import tr, globals
from mcdreforged.api.all import *
from . import psi, plgSelf
from ..reporter import send_matrix
from ..receiver import getMsg


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
            Literal('status')
            .runs(
                lambda src: src.reply(statusSync())
            )
        )
        .then(
            Literal('stop')
            .runs(
                lambda src: src.reply(stopSync(src))
            )
        )
        .then(
            Literal('send')
            .then(
                QuotableText('message')
                .runs(
                    lambda src, ctx: src.reply(send_command(ctx["message"]))
                )
            )
        )
    )

def send_command(message: str):
    send_matrix(message)
    return tr("debug.send_command")

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
    if not globals.tLock.locked():
        globals.report_matrix = True
        start_room_msg()
        return tr("manual_sync.start_sync")
    else:
        return tr("manual_sync.start_error")

def statusSync():
    if globals.report_matrix is True:
        return tr("sync_tips.msync_running")
    else:
        return tr("sync_tips.msync_stopped")

def exit_sync():
    try:
        if globals.sync_task is not None:
            globals.sync_task.cancel()
            globals.report_matrix = False
            globals.sync_task = None
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
    with globals.tLock:
        globals.report_matrix = True
        asyncio.run(on_room_msg())

async def on_room_msg():
    if globals.sync_task is not None and not globals.sync_task.done():
        globals.sync_task.cancel()
        await globals.sync_task
    globals.sync_task = asyncio.create_task(getMsg())
    await globals.sync_task