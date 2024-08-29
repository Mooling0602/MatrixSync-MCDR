import asyncio
import re
import json
import matrix_sync.client

from mcdreforged.api.all import *
from atl_api import parseKey, parseValue
from matrix_sync.reporter import sendMsg

psi = ServerInterface.psi()

lang_files = {
    "raw_lang": "server/plugins/Geyser-Spigot/locales/en_us.json",
    "translated_lang": "server/plugins/Geyser-Spigot/locales/zh_cn.json"
}

config = psi.load_config_simple("config.json", lang_files)

raw_lang = config["raw_lang"]
translated_lang = config["translated_lang"]

death_messages = {}

def on_load(server: PluginServerInterface, old):
    server.logger.info("MatrixSync子包: [MSync]DeathTips 已加载")
    server.logger.info("本插件仅供简体中文用户使用")
    server.logger.info("语言文件默认使用Geyser配置，若未使用Geyser请自行配置语言文件及其路径")

def on_info(server: PluginServerInterface, info: Info):
    global death_messages
    if info.is_from_server:
        key, groups = match_death_msg(raw_lang, info.content)
        if key:
            deathRawFormat = parseValue(raw_lang, key)
            deathMsg = parseValue(translated_lang, key)
            partten_deathRawFormat = re.compile(r"%(\d+)\$s")
            matches_deathRawFormat = partten_deathRawFormat.findall(deathRawFormat)
            regex_template = re.escape(deathRawFormat)
            regex_template = regex_template.replace(r"%1\$s", r"(.+)").replace(r"%2\$s", r"(.+)").replace(r"%3\$s", r"\[(.+)\]|(.+)")
            content_matches = re.match(regex_template, info.content)
            if content_matches:
                placeholder_to_content = {int(matches_deathRawFormat[i]): content_matches.group(i + 1) for i in range(len(matches_deathRawFormat))}
                deathTip = deathMsg
                for placeholder, content in placeholder_to_content.items():
                    placeholder_str = f"%{placeholder}$s"
                    if placeholder_str == "%2$s":
                        contentKey = parseKey(raw_lang, content)
                        tr_content = parseValue(translated_lang, contentKey)
                        if tr_content is not None:
                            content = tr_content
                        else:
                            content = content
                    # if placeholder_str == "%3$s":
                        # content = re.escape(content)
                    deathTip = deathTip.replace(placeholder_str, content)
                    # 修正部分
                    if re.fullmatch(r'(.+)被(.+) using \[(.+)\]|(.+)杀死了', deathTip):
                        match = re.fullmatch(r'(.+)被(.+) using (.+)杀死了', deathTip)
                        if match:
                            player = match.group(1)
                            killer = match.group(2)
                            weapon = match.group(3)
                            deathTip = f"{player}被{killer}用{weapon}杀死了"        
                clientStatus = matrix_sync.client.clientStatus
                if clientStatus:
                    asyncio.run(sendMsg(deathTip))

def match_death_msg(lang, content):
    global death_messages
    with open(lang, 'r') as file:
        lang = file.read()
    lang = json.loads(lang)
    for key in lang.keys():
        if key.startswith("death."):
            value = lang.get(key, None)
            if value:
                value = re.sub(r'%(\d+)\$s', r'(?P<var\1>.+)', value)
                death_messages[key] = value
                for key, value in death_messages.items():
                    match = re.fullmatch(value, content)
                    if match:
                        return key, match.groupdict()
    return None, None
