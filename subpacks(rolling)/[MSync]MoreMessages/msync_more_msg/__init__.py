import re

from matrix_sync.reporter import send_matrix
from mcdreforged.api.all import *

psi = ServerInterface.psi()

def on_load(server: PluginServerInterface, old):
    server.logger.info("Subpack of MatrixSync: [Msync]MoreMessages loaded.")

def on_user_info(server: PluginServerInterface, info: Info):
    formatter(info)
    if gameMsg is not None:
        send_matrix(gameMsg)


def formatter(info: Info):
    global gameMsg
    console_tr = psi.rtr("matrix_sync.tr.cs")
    if info.player is None:
        if re.fullmatch(r'say \S*', info.content):
            msg_content = '{}'.format(info.content.rsplit(' ', 1)[1])
            gameMsg = f"<{console_tr}> {msg_content}"
        else:
            option = psi.rtr("matrix_sync.on_console.commands")
            gameMsg = f"[!] {console_tr} {option} -> {info.content}"
        if info.content == "stop":
            gameMsg = psi.rtr("matrix_sync.sync_tips.server_stopping")
    else:
        if info.content.startswith("!!"):
            option = psi.rtr("matrix_sync.on_console.commands")
            gameMsg = f"[!] {info.player} {option} -> {info.content}"
        else:
            return None