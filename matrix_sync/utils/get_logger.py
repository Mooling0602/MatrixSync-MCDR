import matrix_sync.plg_globals as plg_globals

from mutils.rc_api import psiLogger, srcReply, cmdReply
from mutils.logger import LogLevel, SimpleLogger

def console_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        logger = psiLogger()
        return logger
    else:
        if plg_globals.settings["log_style"]["debug"]:
            logger = SimpleLogger(level=LogLevel.DEBUG, log_format="[{prefix} {level}] {message}", prefix="MSync")
            if plg_globals.settings["log_style"]["show_time"]:
                logger = SimpleLogger(level=LogLevel.DEBUG, log_format="[{prefix}] [{timestamp} {level}] {message}", prefix="MSync")
        else:
            logger = SimpleLogger(log_format="[{prefix} {level}] {message}", prefix="MSync")
            if plg_globals.settings["log_style"]["show_time"]:
                logger = SimpleLogger(log_format="[{prefix}] [{timestamp} {level}] {message}", prefix="MSync")
        return logger

def reply_logger():
    if plg_globals.settings["log_style"]["mcdr"]:
        logger = srcReply()
        return logger
    else:
        logger = cmdReply()
        return logger