import matrix_sync.plg_globals as plg_globals

from mcdreforged.api.types import CommandSource
from ..utils import psi
from . import info_logger, debug_logger


class psiLogger:

    def info(self, *args):
        psi.logger.info(args[0])

    def warning(self, *args):
        psi.logger.warning(args[0])
    
    def error(self, *args):
        psi.logger.error(args[0])

    def critical(self, *args):
        psi.logger.critical(args[0])

    def debug(self, *args):
        psi.logger.debug(args[0])

class srcReply:
    def __call__(self, src: CommandSource, *args):
        src.reply(args[0])

class plgReply:
    def __call__(self, src: CommandSource, *args):
        if src.player is not None:
            psi.tell(src.player, args[0])
        else:
            raise ValueError

def console_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        logger = psiLogger()
        return logger
    else:
        if plg_globals.settings["log_style"]["debug"]:
            logger = debug_logger
        else:
            logger = info_logger
        return logger

def reply_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        logger = srcReply()
        return logger
    else:
        logger = plgReply()
        return logger