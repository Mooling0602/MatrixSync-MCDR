import matrix_sync.plg_globals as plg_globals

from ..utils import psi
from . import info_logger, debug_logger


class psiLogger:

    def info(self, *args):
        psi.logger.info(args[0])

    def warning(self, *args):
        psi.logger.warning(args[0])
    
    def error(self, *args):
        psi.logger.error(args[0])

def get_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        logger = psiLogger()
        return logger
    else:
        if plg_globals.settings["log_style"]["debug"]:
            logger = debug_logger
        else:
            logger = info_logger
        return logger


__all__ = ["get_logger"]
import sys
sys.modules[__name__] = get_logger