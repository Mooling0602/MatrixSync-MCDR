import matrix_sync.plg_globals as plg_globals

from .default import *
from ..utils import *


async def load_config(server: PluginServerInterface):
    plg_globals.config = server.load_config_simple('config.json', account_config)
    if plg_globals.config == account_config:
        server.unload_plugin(plgSelf.id)
    plg_globals.settings = server.load_config_simple('settings.json', default_settings)
    if not plg_globals.settings["log_style"]["mcdr"]:
        psi.logger.info("Plugin MatrixSync will use its logger, with different format to MCDR.")