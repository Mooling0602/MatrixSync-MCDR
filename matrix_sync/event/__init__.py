from ..logger.get_logger import console_logger
from mcdreforged.api.all import *
from ..utils import psi


class room_info(Serializable):
    id: str
    display_name: str
    
class MatrixMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room_info):
        super().__init__('MatrixRoomMessage')
        self.message = message
        self.sender = sender
        self.room_info = room_info

def event_dispatcher(event: type[PluginEvent], *args, **kwargs):
    logger = console_logger()
    event_instance = event(*args, **kwargs)
    psi.dispatch_event(event_instance, args)
    logger.debug("Event dispatched to MCDR!")