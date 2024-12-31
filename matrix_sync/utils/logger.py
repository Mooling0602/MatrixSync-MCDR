import logging
import re
import matrix_sync.plg_globals as plg_globals

from mcdreforged.api.rtext import RText, RColor, RColorRGB
from datetime import datetime
from matrix_sync.utils.text import mc_to_ansi


mc_code_pattern = re.compile(r'§[0-9a-v]')

def ansi_colored_text(text: str, color: type[RColor]) -> str:
    return RText(text, color).to_colored_text()

class CustomFormatter(logging.Formatter):
    def format(self, record):

        record.custom_time = datetime.now().strftime("%H:%M:%S")

        if record.levelname == "INFO":
            record.colored_levelname = f"{ansi_colored_text(record.levelname, RColor.green)}"
        elif record.levelname == "ERROR":
            record.colored_levelname = f"{ansi_colored_text(record.levelname, RColor.red)}"
        elif record.levelname == "WARNING":
            record.colored_levelname = f"{ansi_colored_text(record.levelname, RColorRGB.from_rgb(255, 165, 0))}"
        elif record.levelname == "DEBUG":
            record.colored_levelname = f"{ansi_colored_text(record.levelname, RColor.dark_blue)}"
        else:
            record.colored_levelname = record.levelname

        if mc_code_pattern.search(record.msg):
            record.msg = mc_to_ansi(record.msg)
        
        if hasattr(record, "module_name") and record.module_name:
            if plg_globals.settings["log_style"]["show_time"]:
                format_string = "[MSync - %(module_name)s] [%(custom_time)s %(colored_levelname)s] %(message)s"
            else:
                format_string = "[MSync - %(module_name)s/%(colored_levelname)s] %(message)s"
        else:
            if plg_globals.settings["log_style"]["show_time"]:
                format_string = "[MSync - %(custom_time)s %(colored_levelname)s] %(message)s"
            else:
                format_string = "[MSync - %(colored_levelname)s] %(message)s"
        
        self._style._fmt = format_string
        return super().format(record)

formatter = CustomFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("MSync")
logger.addHandler(handler)