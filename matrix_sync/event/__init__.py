import matrix_sync.utils.get_logger as get_logger

from mcdreforged.api.all import *
from ..utils import psi


class MatrixMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room_id: str):
        super().__init__('MatrixRoomMessage')
        self.message = message
        self.sender = sender
        self.room_id = room_id

def event_dispatcher(event: type[PluginEvent], *args, **kwargs):
    logger = get_logger()
    event_instance = event(*args, **kwargs)
    psi.dispatch_event(event_instance, args)
    logger.debug("Event dispatched to MCDR!")