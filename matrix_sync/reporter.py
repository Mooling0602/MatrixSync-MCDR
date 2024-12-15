import asyncio
import re

from mcdreforged.api.decorator import new_thread
from nio import AsyncClient
from .utils import psi, plgSelf, tr, globals
from .utils.token import getToken


# Game Message reporter.
@new_thread('MatrixReporter')
def send_matrix(message):
    asyncio.run(send(message))

async def send(message):
    from .client import clientStatus
    if clientStatus:
        if globals.report_matrix:
            await sendMsg(message)
            psi.logger.debug("消息已发送！")
        else:
            psi.logger.debug("消息未发送：同步未启动")
    else:
        psi.logger.debug("消息未发送：bot未初始化成功")

async def sendMsg(message) -> None:
    from .config import homeserver, user_id, room_id, device_id
    client = AsyncClient(f"{homeserver}")
    user, token = await getToken()
    client.access_token = token
    if user != user_id:
        if user is not None:
            tip = tr("init_tips.user_mismatch")
            psi.logger.error(tip.replace("%user_id%", user_id))
            psi.logger.info(tr("init_tips.do_unload"))
            psi.unload_plugin(plgSelf.id)
        else:
            psi.logger.error(tr("init_tips.token_invaild"))
            psi.logger.info(tr("init_tips.do_unload"))
            psi.unload_plugin(plgSelf.id)
    else:
        client.user_id = user_id
        client.device_id = device_id

    pattern = re.compile(r'§[0-9a-v]')

    message_to_send = re.sub(pattern, '', message)

    await client.room_send(
        room_id,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": message_to_send},
    )

    await client.close()
