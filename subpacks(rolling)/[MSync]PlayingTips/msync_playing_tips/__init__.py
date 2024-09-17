import matrix_sync.client
import asyncio
from matrix_sync.reporter import sendMsg
from mcdreforged.api.all import *

def on_load(server: PluginServerInterface, old):
    server.logger.info("Subpack of MatrixSync: playing_tips loaded.")

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    tip = f"[+]{player}"
    if matrix_sync.client.clientStatus:
        asyncio.run(sendMsg(tip))

def on_player_left(server: PluginServerInterface, player: str):
    tip = f"[-]{player}"
    if matrix_sync.client.clientStatus:
        asyncio.run(sendMsg(tip))