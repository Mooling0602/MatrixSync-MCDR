from typing import Optional
from mcdreforged.api.types import ServerInterface


psi = ServerInterface.psi()
MCDRConfig = psi.get_mcdr_config()
plgSelf = psi.get_self_metadata()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()

def tr(key: str, return_str: Optional[bool] = True):
    if key.startswith("#"):
        result = psi.rtr(key.replace("#", ""))
    else:
        result = psi.rtr(f"{plgSelf.id}.{key}")
    if return_str is True:
        result = str(result)
    return result
    