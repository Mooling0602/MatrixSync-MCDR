# 导入所需的API
import asyncio
import json
import re
import os
import sys
import aiofiles

from mcdreforged.api.all import *
from nio import AsyncClient, LoginResponse, MatrixRoom, RoomMessageText

psi = ServerInterface.psi()

# 默认配置内容
default_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org"
}

# 加载插件并初始化配置文件
def on_load(server: PluginServerInterface, old):
    global config, DATA_FOLDER, DATA_FILE, homeserver

    config = server.load_config_simple("config.json", default_config)
    DATA_FOLDER = server.get_data_folder()
    server.logger.info(f"配置文件及登录缓存数据路径: {DATA_FOLDER}")
    DATA_FILE = f"{DATA_FOLDER}/token.json"
    homeserver = config["homeserver"]
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + config["homeserver"]

    check_config(server)

# 检查配置文件
def check_config(server: PluginServerInterface):
    if config["homeserver"] == "https://matrix.example.org" or config["user_id"] == "@username:matrix.example.org" or config["password"] == "your_password" or config["room_id"] == "!your-room_id:matrix.example.org":
        server.logger.info("请修改好所有配置项，然后重新加载插件! ")
        server.unload_plugin("matrix_sync")
    else:
        server.logger.info("正在应用当前配置，请稍后...")

# 写入缓存
def cache_data(resp: LoginResponse):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "token": resp.access_token
            },
            f,
        )
    
# 初始化Matrix机器人
async def init_client(server: PluginServerInterface) -> None:
    if not os.path.exists(DATA_FILE):
        server.logger.info("检测到首次登录, 使用账号密码登录中...")
        user_id = config["user_id"]
        password = config["password"]
        
        client = AsyncClient(homeserver, user_id)
        resp = await client.login(password, device_name="matrix-nio")
        
        if isinstance(resp, LoginResponse):
            server.logger.info("登录成功, 正在写入缓存以供稍后和下次登录使用...")
            cache_data(resp)
            server.logger.info("缓存写入完成! ")
        else:
            server.logger.info(f"机器人登录失败: {resp}")
            server.logger.info(f'根服务器: "{homeserver}", 登录用户: "{user_id}"')
            server.logger.info("请检查账号密码信息是否正确, 并确认网络是否正常, 若有问题可以发issue获取帮助.")
            sys.exit(1)

    else:
        async with aiofiles.open(DATA_FILE, "r") as f:
            contents = await f.read()
        cache = json.loads(contents)
        client = AsyncClient(f"{homeserver}")
        client.access_token = cache["token"]
        client.user_id = config["user_id"]
        client.device_id = "matrix-nio"
        room_id = config["room_id"]

        message = "MC服务器已启动！"
        
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )
        
        global test_status
        test_status = True
        if test_status:
            server.logger.info("机器人登录成功，已向群组发送测试消息.")
    await client.close()


# 检测连接和登录情况，并反馈状态
def on_server_startup(server: PluginServerInterface):
    asyncio.run(init_client(server))
    if test_status:
        asyncio.run(get_msg())

        
def on_user_info(server: PluginServerInterface, info: Info):
        # server.logger.info("检测到玩家消息, 正在尝试发送到Matrix群组...")
        # 取消上面的注释以判断线上的游戏消息是否开始上报
        global message
        message = f"<{info.player}> {info.content}"
        if info.player is None:
            message = f"<Console> {info.content}"
        flag = False
        if test_status:
            flag = True
        if flag:
            asyncio.run(send_msg(server))

# 消息上报器
async def send_msg(server: PluginServerInterface) -> None:
    async with aiofiles.open(DATA_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = config["user_id"]
    client.device_id = "matrix-nio"
    room_id = config["room_id"]

    await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
    )

    await client.close()

# i18n将在正式版本v1.1.0以后使用
# Translations will be available in ver 1.1.0 and later.

# 消息接收器
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    room_msg = f"[MatrixSync] {room.user_name(event.sender)}: {event.body}"
    psi.broadcast(f"{room_msg}")

async def get_msg() -> None:
    async with aiofiles.open(DATA_FILE, "r") as f:
        contents = await f.read()
    cache = json.loads(contents)
    client = AsyncClient(f"{homeserver}")
    client.access_token = cache["token"]
    client.user_id = config["user_id"]
    client.device_id = "matrix-nio"
    room_id = config["room_id"]

    client.add_event_callback(message_callback, RoomMessageText)
    await client.sync_forever(timeout=0)

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code != 0:
        asyncio.close(get_msg())
