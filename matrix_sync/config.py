from .utils import psi

lock_is_None = True

# Default config.
account_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org",
    "room_name": "your-room-display-name",
    "device_id": "mcdr"
}

# Bot manage config.
bot_config = {
    "plugin_enabled": False,
    "allow_all_rooms_msg": False,
    "sync_old_msg": False,
    "room_msg_format": {
        "single_room": "[MSync] %sender%: %message%",
        "multi_room": "[MSync|%room_display_name%] %sender%: %message%"
    }
}

def load_config():
    global config, user_id, password, room_id, room_name, settings, use_token, DATA_FOLDR, TOKEN_FILE, device_id, homeserver, load_tip, sync_old_msg
    config = psi.load_config_simple("config.json", account_config)
    user_id = config["user_id"]
    password = config["password"]
    room_id = config["room_id"]
    room_name = config["room_name"]
    settings = psi.load_config_simple("settings.json", bot_config)
    sync_old_msg = settings["sync_old_msg"]
    DATA_FOLDER = psi.get_data_folder()
    tip_path = psi.rtr("matrix_sync.init_tips.config_path")
    load_tip = f"{tip_path}: {DATA_FOLDER}"
    TOKEN_FILE = f"{DATA_FOLDER}/token.json"
    device_id = config["device_id"]
    homeserver = config["homeserver"]
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + config["homeserver"]

# Check the config.
def check_config():
    global lock_is_None, do_unload
    if not settings["plugin_enabled"]:
        lock_is_None = True
        psi.logger.info(psi.rtr("matrix_sync.init_tips.need_edit_config"))
        do_unload = True
    else:
        lock_is_None = False
        do_unload = False
        psi.logger.info(psi.rtr("matrix_sync.init_tips.read_config"))
