from . import *
from mcdreforged.api.all import *

psi = ServerInterface.psi()
plgSelf = psi.get_self_metadata()

def tr(tr_key: str):
    translation = psi.rtr(f"{plgSelf.id}.{tr_key}")
    translation: str = str(translation)
    return translation