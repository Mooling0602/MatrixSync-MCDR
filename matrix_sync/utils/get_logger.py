import logging
import matrix_sync.utils.logger as plg_logger
import matrix_sync.plg_globals as plg_globals

from . import psi
from .logger import CustomFormatter


def get_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        return psi.logger
    else:
        if plg_logger.logger is None:
            formatter = CustomFormatter()
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            new_logger = logging.getLogger("MSync")
            log_level = logging.INFO if not plg_globals.settings["log_style"]["debug"] else logging.DEBUG
            new_logger.setLevel(log_level)
            new_logger.addHandler(handler)
            plg_logger.logger = new_logger
            return new_logger
        else:
            return plg_logger.logger

    
__all__ = ["get_logger"]
import sys
sys.modules[__name__] = get_logger