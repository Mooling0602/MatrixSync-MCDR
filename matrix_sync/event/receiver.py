import matrix_sync.logger.get_logger as get_logger
import matrix_sync.plg_globals as plg_globals

from mcdreforged.api.types import PluginServerInterface


def listen_message(server: PluginServerInterface):
    server.register_event_listener("MatrixRoomMessage", on_matrix_message)

def on_matrix_message(server, message: str, sender: str, room):
    logger = get_logger()
    if plg_globals.settings["listen"]["all_rooms"]:
        message_format = plg_globals.settings["message_format"]["all_room"]
        room_message = message_format.replace('%room_display_name%', room.display_name).replace('%sender%', sender).replace('%message%', message)
    else:
        message_format = plg_globals.settings["message_format"]["single_room"]
        room_message = message_format.replace('%sender%', sender).replace('%message%', message)
    logger.info(room_message, "Message")
    server.say(room_message)