# Send messages to matrix room by configured room_id.
import re
import matrix_sync.plg_globals as plg_globals

from . import get_homeserver
from .init import check_token
from ..utils import *
from ..utils.logger import *
from ..utils.token import getToken
from nio import AsyncClient


async def send_to_matrix(message) -> None:
    client = AsyncClient(get_homeserver(plg_globals.config["homeserver"]))
    token_vaild = await check_token()
    if token_vaild:
        user, token = await getToken()

        client.user_id = plg_globals.config["user_id"]
        client.access_token = token
        client.device_id = plg_globals.config["device_id"]

        # Remove formatting code of mc for colorful text not supported yet.
        pattern = re.compile(r'§[0-9a-v]')
        message_to_send = re.sub(pattern, '', message)

        await client.room_send(
            plg_globals.config["room_id"],
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": message_to_send},
        )

        await client.close()