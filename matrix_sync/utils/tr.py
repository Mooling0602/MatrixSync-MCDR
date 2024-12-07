from mcdreforged.api.all import *

psi = ServerInterface.psi()
plgSelf = psi.get_self_metadata()

def main(tr_key: str):
    translation = psi.rtr(f"{plgSelf.id}.{tr_key}")
    translation: str = str(translation)
    return translation

__all__ = ['main']