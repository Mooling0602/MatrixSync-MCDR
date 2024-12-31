import logging

import matrix_sync.plg_globals as plg_globals
import matrix_sync.utils.logger as plg

from . import psi


def get_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        return psi.logger
    else:
        log_level = logging.INFO if not plg_globals.settings["log_style"]["debug"] else logging.DEBUG
        plg.logger.setLevel(log_level)
        if plg.logger.level != log_level:
            plg.logger.setLevel(log_level)
        return plg.logger
    
__all__ = ["get_logger"]
import sys
sys.modules[__name__] = get_logger