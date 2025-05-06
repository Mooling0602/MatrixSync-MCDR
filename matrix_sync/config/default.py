# Default config.
account_config = {
    "homeserver": "https://matrix.example.org",
    "user_id": "@username:matrix.example.org",
    "password": "your_password",
    "room_id": "!your-room_id:matrix.example.org",
    "device_id": "mcdr"
}

# Default settings.
default_settings = {
    "listen": {
        "all_rooms": True,
        "old_messages": False
    },
    "message_format": {
        "single_room": "%sender%: %message%",
        "all_room": "[%room_display_name%] %sender%: %message%",
        "game_chat": "[MC] <%player_name%> %message%"
    },
    "log_style": {
        "mcdr": False,
        "debug": False,
        "show_time": False
    },
    "ver": "2.5.4"
}