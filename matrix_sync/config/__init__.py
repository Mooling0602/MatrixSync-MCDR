import asyncio
import os
import matrix_sync.plg_globals as plg_globals

from .default import *
from ..utils import *
from ..client.init import check_token
from mcdreforged.api.types import PluginServerInterface


def load_config(server: PluginServerInterface):
    plg_globals.config = server.load_config_simple('config.json', account_config)
    if plg_globals.config == account_config:
        server.unload_plugin(plgSelf.id)
    plg_globals.settings = server.load_config_simple('settings.json', default_settings)
    if plg_globals.settings["ver"] != "2.5.1" and plg_globals.settings["ver"] != "2.5.4":
        plg_globals.settings = None
        psi.logger.info(tr("settings_comp_check.failed"))
        os.rename(f"{configDir}/settings.json", f"{configDir}/settings.json.bak")
        plg_globals.settings = server.load_config_simple('settings.json', default_settings)
    if not plg_globals.settings["log_style"]["mcdr"]:
        psi.logger.info("Plugin MatrixSync will use its logger, different with MCDR.")
    if os.path.exists(f"{configDir}/token.json"):
        plg_globals.token_vaild = asyncio.run(add_check_task())

async def add_check_task() -> bool:
    result = await check_token()
    return result