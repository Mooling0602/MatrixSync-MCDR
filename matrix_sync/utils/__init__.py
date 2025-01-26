from mcdreforged.api.types import ServerInterface
from mutils import tr

psi = ServerInterface.psi()
MCDRConfig = psi.get_mcdr_config()
plgSelf = psi.get_self_metadata()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()