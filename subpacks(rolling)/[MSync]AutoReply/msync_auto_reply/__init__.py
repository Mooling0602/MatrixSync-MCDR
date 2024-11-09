import os
import matrix_sync.config
import matrix_sync.client
import yaml
from mcdreforged.api.all import *
from matrix_sync.reporter import send_matrix

CONFIG_PATH = 'config/matrix_sync/auto_reply/config.yml'

DEFAULT_CONFIG = {
    "triggers": {
        "触发词1": "回复内容1",
        "触发词2": "回复内容2",
        "触发词3": "回复内容3"
    }
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as config_file:
            yaml.dump(DEFAULT_CONFIG, config_file, allow_unicode=True)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        return yaml.safe_load(config_file)

def on_load(server: PluginServerInterface, old):
    global plugin_config
    plugin_config = load_config()
    
    server.logger.info("[MSync]AutoReply loaded.")
    server.register_event_listener('MatrixRoomMessage', main)

def main(server: PluginServerInterface, message: str, sender: str):
    user_id = matrix_sync.config.user_id
    triggers = plugin_config.get("triggers", {})

    if sender != user_id:
        for trigger_word, reply_content in triggers.items():
            if message == trigger_word:
                clientStatus = matrix_sync.client.clientStatus
                if clientStatus:
                    send_matrix(reply_content)
                    server.logger.info("解析到指定内容，已自动发送回复")
                break