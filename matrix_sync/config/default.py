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
    "sync": {
        "all_rooms": True,
        "old_messages": False
    },
    "message_format": {
        "single_room": "%sender%: %message%",
        "all_room": "[%room_display_name%] %sender%: %message%"
    },
    "log_style": {
        "mcdr": False,
        "debug": False
    }
}