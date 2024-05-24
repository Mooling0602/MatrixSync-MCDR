import matrix_sync.client
import asyncio
from functools import partial
from matrix_sync.reporter import sendMsg
from mcdreforged.api.all import *

def on_load(server: PluginServerInterface, old):
    server.logger.info("Subpack of MatrixSync: playing_tips loaded.")

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    tip = f"[+]{player}"
    if matrix_sync.client.clientStatus:
        asyncio.run(sendMsg(tip))
    else:
        server.logger.info("Main plugin not inited or some error happened.")
        server.logger.info("Please reload this subpack after make sure message sync works normally.")
        server.unload_plugin("matrix_playing_tips")

def on_player_left(server: PluginServerInterface, player: str):
    tip = f"[-]{player}"
    if matrix_sync.client.clientStatus:
        asyncio.run(sendMsg(tip))
    else:
        server.logger.info("Main plugin not inited or some error happened.")
        server.logger.info("Please reload this subpack after make sure message sync works normally.")
        server.unload_plugin("matrix_playing_tips")