import asyncio

from . import builder, tr, globals
from mcdreforged.api.all import *
from . import psi, plgSelf
from ..reporter import send_matrix
from ..receiver import getMsg


def plugin_command(server: PluginServerInterface):
    help_message = tr("help_tips.message", False)
    server.register_help_message("!!msync", help_message)
    builder.arg("message", QuotableText)
    builder.register(server)

@builder.command("!!msync send <message>")
def send_command(src: CommandSource, ctx: CommandContext):
    send_matrix(ctx["message"])
    src.reply(tr("debug.send_command"))

# Help tips.
@builder.command("!!msync")
@builder.command("!!msync help")
def show_help(src: CommandSource):
    pfx = f"{plgSelf.id}.help_tips"
    src.reply(RTextList(
        tr(f"{pfx}.title", False) + "\n",
        tr(f"{pfx}.root_command", False) + "\n",
        tr(f"{pfx}.start_command", False) + "\n",
        tr(f"{pfx}.stop_command", False) + "\n",
        tr(f"{pfx}.send_command", False) + "\n",
        tr(f"{pfx}.status_command", False) + "\n"
    ))

# Manually run sync processes.
@builder.command("!!msync start")
def manualSync(src: CommandSource):
    if not globals.tLock.locked():
        globals.report_matrix = True
        start_room_msg()
        src.reply(tr("manual_sync.start_sync"))
    else:
        src.reply(tr("manual_sync.start_error"))

@builder.command("!!msync status")
def syncStatus(src: CommandSource):
    if globals.report_matrix is True:
        src.reply(tr("sync_tips.msync_running"))
    else:
        src.reply(tr("sync_tips.msync_stopped"))

def exit_sync():
    try:
        if globals.sync_task is not None:
            globals.sync_task.cancel()
            globals.report_matrix = False
            globals.sync_task = None
            return tr("manual_sync.stop_sync")
        else:
            return tr("manual_sync.not_running")
    except Exception as e:
        psi.logger.error(f"Error exit {plgSelf.id}: {e}")
        return tr("manual_sync.stop_error")

# Manually stop sync processes.
@builder.command("!!msync stop")
def stopSync(src):
    if src.is_console:
        response =  exit_sync()
        src.reply(response)
    else:
        src.reply(tr("manual_sync.stop_denied"))

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