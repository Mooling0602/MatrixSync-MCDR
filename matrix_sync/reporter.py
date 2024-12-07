import asyncio
import re

from mcdreforged.api.all import *
from nio import AsyncClient
from .utils.token import getToken


# Game Message reporter.
@new_thread('MatrixReporter')
def send_matrix(message):
    asyncio.run(send(message))

async def send(message):
    await sendMsg(message)

async def sendMsg(message) -> None:
    from .config import homeserver, user_id, room_id, device_id
    client = AsyncClient(f"{homeserver}")
    client.access_token = await getToken()
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
