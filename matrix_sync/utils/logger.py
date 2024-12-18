from . import *


def log_tool(log_text: str, color: RColor, pfx: str, prefix: Optional[str] = None):
    if globals.settings["log_style"]["mcdr"]:
        if pfx == "Info":
            if prefix == "Message":
                log_text = "[MSync] " + log_text
            psi.logger.info(log_text)
        elif pfx == "Warning":
            psi.logger.warning(log_text)
        elif pfx == "Error":
            psi.logger.error(log_text)
        else:
            psi.logger.info(log_text)
    else:
        pfx_with_color = RText(pfx, color).to_colored_text()
        if prefix is not None:
            pfx_with_color = f"{prefix}/" + pfx_with_color
        print(f"[MSync - {pfx_with_color}] {log_text}")

def log_info(log_text: str, prefix: Optional[str] = None):
    log_tool(log_text, RColor.green, "Info", prefix)

def log_warning(log_text: str, prefix: Optional[str] = None):
    log_tool(log_text, RColorRGB.from_rgb(255, 165, 0), "Warning", prefix)
    
def log_error(log_text: str, prefix: Optional[str] = None):
    log_tool(log_text, RColor.red, "Error", prefix)