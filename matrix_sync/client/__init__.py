from . import *
from ..utils.token import getToken
from nio import AsyncClient


def get_homeserver(url: str):
    correct_url = url
    if not (url.startswith("https://") or url.startswith("http://")):
        correct_url = "https://" + url
    return correct_url

async def get_client_instance():
    import matrix_sync.plg_globals as plg_globals
    homeserver = get_homeserver(plg_globals.config["homeserver"])
    user = plg_globals.config["user_id"]
    device_id = plg_globals.config["device_id"]
    client_instance = AsyncClient(homeserver, user, device_id)
    user, token = await getToken()
    client_instance.access_token = token
    return client_instance



