import asyncio
import re
import matrix_sync.client

from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg
from gtl_api import parseKey, parseValue, parseContent

psi = ServerInterface.psi()

lang_files = {
    "raw_lang": "server/plugins/Geyser-Spigot/locales/en_us.json",
    "translated_lang": "server/plugins/Geyser-Spigot/locales/zh_cn.json"
}

config = psi.load_config_simple("config.json", lang_files)

raw_lang = config["raw_lang"]
translated_lang = config["translated_lang"]

def on_load(server: PluginServerInterface, old):
    server.logger.info("MatrixSync 子包: AdvancementsTips 已加载")
    server.logger.info("本插件仅供简体中文用户使用")
    server.logger.info("语言文件默认使用Geyser配置，若未使用Geyser请自行获取语言文件并配置其路径")

def on_info(server: PluginServerInterface, info: Info):
    if info.is_from_server and re.fullmatch(r'(.+) has completed the challenge (.+)', info.content):
        match = re.fullmatch(r'(.+) has completed the challenge (.+)', info.content)
        if match:
            player = match.group(1)
            raw_content = match.group(2)
            content = parseContent(raw_content)
            key = parseKey(raw_lang, content)
            tr_content = parseValue(translated_lang, key)
        if matrix_sync.client.clientStatus:
            asyncio.run(sendMsg(f"[!]玩家 {player} 完成了挑战 [{tr_content}]"))
    if info.is_from_server and re.fullmatch(r'(.+) has reached the goal (.+)', info.content):
        match = re.fullmatch(r'(.+) has reached the goal (.+)', info.content)
        if match:
            player = match.group(1)
            raw_content = match.group(2)
            content = parseContent(raw_content)
            key = parseKey(raw_lang, content)
            tr_content = parseValue(translated_lang, key)
        if matrix_sync.client.clientStatus:
            asyncio.run(sendMsg(f"[!]玩家 {player} 达成了目标 [{tr_content}]"))
    if info.is_from_server and re.fullmatch(r'(.+) has made the advancement (.+)', info.content):
        match = re.fullmatch(r'(.+) has made the advancement (.+)', info.content)
        if match:
            player = match.group(1)
            raw_content = match.group(2)
            content = parseContent(raw_content)
            key = parseKey(raw_lang, content)
            tr_content = parseValue(translated_lang, key)
        if matrix_sync.client.clientStatus:
            asyncio.run(sendMsg(f"[!]玩家 {player} 取得了进度 [{tr_content}]"))