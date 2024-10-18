import matrix_sync.config
import matrix_sync.client

from mcdreforged.api.all import *
from matrix_sync.reporter import sender

def on_load(server: PluginServerInterface, old):
    server.logger.info("[MSync]AutoReply loaded.")
    server.register_event_listener('MatrixRoomMessage', main)

def main(server: PluginServerInterface, message: str, sender: str):
    user_id = matrix_sync.config.user_id
    if not sender == user_id:
        if message == "服务器连接信息":
            clientStatus = matrix_sync.client.clientStatus
            if clientStatus:
                sender("服务器名称：星块服务器\n地址：play.staringplanet.top\n* 已进行SRV解析，Java版无需添加端口\n端口：21152")
                server.logger.info("解析到指定内容，已自动发送回复")
