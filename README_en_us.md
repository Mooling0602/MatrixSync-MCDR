- [中文](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README.md)
- English

# MatrixSync-MCDR
A MCDR (full name [MCDReforged](https://mcdreforged.com/)) plugin, use to sync messages between Matrix groups and online gaming in Minecraft servers.

About [Matrix](https://matrix.org/): an open decentralized network communication protocol for chat software.

The following project is used in the development process: [matrix-nio](https://pypi.org/project/matrix-nio/)。

## Usage
Download the latest version from the release, install the necessary Python dependencies in the MCDReforged startup environment, and then throw it into the plugins folder.

Before using this plugin, you must know what [Matrix](https://matrix.org/) is, then prepare an account as a matrix bot for message synchronization, and carefully read the following content to configure the plugin.

After configuration and enabling the plugin, if the test message is successfully sent to the matrix group, it means that message synchronization has started to work.

If there is any issue with message forwarding in any direction during the message synchronization process, please check the configuration according to the following content to ensure it is correct.

### Configuration File
#### config.json

| Configuration Item | Content |
| - | - |
| **homeserver** | The home server used to log in to the bot account |
| **user_id** | The bot account ID, formatted as @username:example.com |
| **password** | The password of the bot account, generally only used for the initial login |
| **room_id** | The ID of the room to receive game messages, currently only one can be set |
| **room_name** | The display name of the room to forward messages to the game (must be accurate, if updated, it also needs to be modified synchronously, otherwise you may not see any messages), currently only one can be set |
| **device_id** | The device name used for login, generally no need to modify, can be customized |

#### settings.json

| Configuration Item | Content |
| - | - |
| plugin-enabled | Whether the plugin is enabled, please ensure the configuration file and necessary settings are modified correctly before enabling |
| allow_all_rooms_msg | Whether to allow messages from all rooms, if enabled, messages from rooms joined by the bot account will be forwarded to the game, with the room display name specified, otherwise only messages from the configured room will be forwarded |

## Interface (API)
The plugin provides a coroutine function `sendMsg()` for other developers to call to send custom content to the Matrix group. Its callback parameter is `message`. Here is the code reference:
```
import asyncio
import ...
from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg
from ... import ...
def main():
    pass
    asyncio.run(sendMsg(message))
```
Replace `message` with the custom content you want to send.

## Note
- Support with bugs for hot reloading will produce a lot of errors, possibly with no actual impact (hoping someone can help fix, PRs are welcome; global reloading of the plugin will also cause this issue)
- If hot reloading, you must manually execute !!msync to continue synchronizing Matrix messages to the game
- When the plugin is loaded for the first time, it will automatically initialize the configuration and unload itself. You need to correctly modify the default configuration file, then restart the server or reload the plugin to use it normally.
- Encrypted messages (EE2E) are not planned to be supported, you can modify the plugin through secondary development if needed.
- Currently supports only Simplified Chinese and English (translated from Chinese by Google), anyone can contact me to help translate.

