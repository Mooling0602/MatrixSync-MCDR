import datetime

from typing import Optional
from mcdreforged.api.rtext import *
from .text import *


class SimpleLogger:
    def __init__(self, level="INFO"):
        self.level = level
        self.levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}
        self.colors = {
            "DEBUG": RColor.dark_blue,
            "INFO": RColor.green,
            "WARNING": RColorRGB.from_rgb(255, 165, 0),
            "ERROR": RColor.red,
            "RESET": RColor.reset
        }

    def log(self, level, message: str, module: Optional[str]=None):
        if self.levels[level] >= self.levels[self.level]:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            color = self.colors.get(level, self.colors["RESET"])
            colored_level = RText(level, color).to_colored_text()
            if pattern.search(message):
                message = mc_to_ansi(message)
            if module is not None:
                print(f"[MSync - {module}] [{timestamp} {colored_level}] {message}")
            else:
                print(f"[MSync - {timestamp} {colored_level}] {message}")

    def debug(self, message, module: Optional[str]=None):
        if module is None:
            self.log("DEBUG", message)
        else:
            self.log("DEBUG", message, module)

    def info(self, message, module: Optional[str]=None):
        if module is None:
            self.log("INFO", message)
        else:
            self.log("INFO", message, module)

    def warning(self, message, module: Optional[str]=None):
        if module is None:
            self.log("WARNING", message)
        else:
            self.log("WARNING", message, module)

    def error(self, message, module: Optional[str]=None):
        if module is None:
            self.log("ERROR", message)
        else:
            self.log("ERROR", message, module)

info_logger = SimpleLogger(level="INFO")
debug_logger = SimpleLogger(level="DEBUG")
# info_logger.error("Error", "Main")
# debug_logger.debug("Debug", "Main")