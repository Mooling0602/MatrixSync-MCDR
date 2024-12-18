import matrix_sync.globals as globals

from .default import *
from ..utils import *


async def load_config(server: PluginServerInterface):
    globals.config = server.load_config_simple('config.json', account_config)
    if globals.config == account_config:
        server.unload_plugin(plgSelf.id)
    globals.settings = server.load_config_simple('settings.json', default_settings)
    if not globals.settings["log_style"]["mcdr"]:
        psi.logger.info("Plugin MatrixSync will use its logger, with different format to MCDR.")