from mcdreforged.api.all import *
from typing import Optional
from ..utils import psi


class MatrixMessageEvent(PluginEvent):
    def __init__(self, message: str, sender: str, room_name: Optional[str] = None):
        super().__init__('MatrixRoomMessage')
        self.message = message
        self.sender = sender
        self.room_name = room_name

class SendToMatrixEvent(PluginEvent):
    def __init__(self, user_id: str, message: Optional[str] = None):
        super().__init__('MessageSendToMatrix')
        self.user_id = user_id
        self.message = message

def event_dispatcher(event: type[PluginEvent], *args, **kwargs):
    event_instance = event(*args, **kwargs)
    psi.dispatch_event(event_instance, args)
    psi.logger.debug("Event dispatched to MCDR!")