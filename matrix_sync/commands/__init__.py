import asyncio
import threading
import matrix_sync.plg_globals as plg_globals

from mcdreforged.api.all import *
from ..utils.get_logger import console_logger, reply_logger
from ..client.reporter import send_to_matrix
from ..client.receiver import get_messages, stop_sync
from ..utils import psi, plgSelf, tr
from .help import *


builder = SimpleCommandBuilder()

plg_globals.tLock = threading.Lock()

def start_sync():
    logger = console_logger()
    if not plg_globals.tLock.locked():
        run_sync_task()
    else:
        logger.warning(tr("on_sync_running"))

@new_thread('MatrixReceiver')
def run_sync_task():
    logger = console_logger()
    plg_globals.sync = True
    if plg_globals.token_vaild:
        with plg_globals.tLock:
            logger.info(tr("on_sync_start"))
            asyncio.run(add_sync_task())
    else:
        logger.error(tr("token_mismatch"))
        plg_globals.sync = False

async def add_sync_task():
    await get_messages()

@new_thread('MatrixReporter')
def matrix_reporter(message: str):
    asyncio.run(add_report_task(message))

async def add_report_task(message: str):
    report_task = asyncio.create_task(send_to_matrix(message))
    await report_task

def command_register(server: PluginServerInterface):
    server.register_help_message("!!msync", help_message)
    builder.arg("message", QuotableText)
    builder.arg("pack_name", Text)
    builder.register(server)

@builder.command("!!msync start")
def on_command_start(src: CommandSource):
    if src.has_permission_higher_than(2):
        start_sync()
    else:
        src.reply(tr("no_permission"))

@builder.command("!!msync stop")
async def on_command_stop(src: CommandSource):
    if src.has_permission_higher_than(2):
        await stop_sync()
    else:
        src.reply(tr("no_permission"))

@builder.command("!!msync status")
def show_status(src: CommandSource):
    logger = console_logger()
    def return_result():
        if plg_globals.sync:
            logger.info(tr("sync_status.running"))
        else:
            logger.info(tr("sync_status.not_running"))
    if src.is_console:
        logger = console_logger()
        logger.info(f"Receiver: {plg_globals.sync}")
        return_result()
    if src.is_player:
        reply = reply_logger()
        reply.log(src, f"Receiver: {plg_globals.sync}", logger)
        if plg_globals.sync:
            reply.log(src, tr("sync_status.running"), logger)
        else:
            reply.log(src, tr("sync_status.not_running"), logger)

@builder.command("!!msync send <message>")
def on_command_send(src: CommandSource, ctx: CommandContext):
    if src.has_permission_higher_than(2):
        if plg_globals.token_vaild:
            matrix_reporter(ctx["message"])
            src.reply(tr("on_send_command.sending"))
        else:
            src.reply(tr("on_send_command.failed") + ": " + tr("token_mismatch"))
    else:
        src.reply(tr("no_permission"))

@builder.command("!!msync reload")
def on_command_reload(src: CommandSource):
    if src.has_permission_higher_than(2):
        psi.reload_plugin(plgSelf.id)
    else:
        reply = reply_logger()
        logger = console_logger()
        reply.log(src, tr("no_permission"), logger)

@builder.command("!!msync reload <pack_name>")
def on_command_reload_subpack(src: CommandSource, ctx: CommandContext):
    if src.has_permission_higher_than(2):
        plugin_list = psi.get_plugin_list()
        subpack_id = ctx["pack_name"]
        if not subpack_id.startswith("msync_"):
            subpack_id = "msync_" + ctx["pack_name"]
        if subpack_id in plugin_list:
            psi.reload_plugin(subpack_id)
        else:
            src.reply("Reload subpack error: Invaild name or target subpack is not loaded!")
    else:
        src.reply(tr("no_permission"))

@builder.command("!!msync")
@builder.command("!!msync help")
def show_help(src: CommandSource):
    src.reply(help_page)