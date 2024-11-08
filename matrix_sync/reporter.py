import asyncio
import matrix_sync.config

from mcdreforged.api.all import *
from nio import AsyncClient
from matrix_sync.utils.token import getToken
from matrix_sync.utils.globals import psi

# Game Message reporter.
@new_thread('MatrixReporter')
def sender(message):
    asyncio.run(send(message))

async def send(message):
    await sendMsg(message)

async def sendMsg(message) -> None:
    homeserver = matrix_sync.config.homeserver
    user_id = matrix_sync.config.user_id
    room_id = matrix_sync.config.room_id
    device_id = matrix_sync.config.device_id
    client = AsyncClient(f"{homeserver}")
    client.access_token = await getToken()
    client.user_id = user_id
    client.device_id = device_id

    try:
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": f"{message}"},
        )

        await client.close()
    except Exception as e:
        psi.logger.error(f"Send to matrix error: {e}")
