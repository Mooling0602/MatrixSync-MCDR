from mcdreforged.api.all import *
from typing import Optional

def on_load(server: PluginServerInterface, old):
    server.logger.info("Subpack of MatrixSync: [MSync]plgDebugger loaded.")
    server.register_event_listener('MatrixRoomMessage', main)

def main(server: PluginServerInterface, message: str, sender: str, room: Optional[str] = None):
    server.logger.info(f"Content: {message}")
    server.logger.info(f"Sender: {sender}")
    if room is not None:
        server.logger.info(f"Room Name: {room}")