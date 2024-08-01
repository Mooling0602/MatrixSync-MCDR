- [中文](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README.md)
- English

# MatrixSync-MCDR
A MCDR (full name [MCDReforged](https://mcdreforged.com/)) plugin, use to sync messages between Matrix groups and online gaming in Minecraft servers.

About [Matrix](https://matrix.org/): an open decentralized network communication protocol for chat software.

The following project is used in the development process: [matrix-nio](https://pypi.org/project/matrix-nio/)。

Thanks for ChatGPT and Google Translate's help to translate the content from Chinese, if anything wrong, please issue to feedback or PR to `/lang`.

Present branch version: main@2.2.0

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
| **room_name** | The display name of the room to forward messages to the game (must be accurate, if updated, it also needs to be modified synchronously, otherwise you will not see any messages), currently only one can be set |
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
import matrix_sync.client
import ...
from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg
from ... import ...
def main():
    pass
    clientStatus = matrix_sync.client.clientStatus
    if clientStatus:
        asyncio.run(sendMsg(message))

# async def main():
#     pass
#     clientStatus = matrix_sync.client.clientStatus
#     if clientStatus:
#         await sendMsg(message)
```
Add the main plugin (MatrixSync) to the dependencies of MCDR, and include its Python dependencies in your plugin as well. Then, during development, replace `message` with the custom content you want to send.

Please note that support for this interface is experimental, and it cannot be guaranteed that the message forwarding functionality of the main plugin (MatrixSync) will work when calling this interface (there may be situations where the bot is not properly configured, or existing login information and tokens cannot be used). If you want to call this interface, please ensure that the user has installed and configured the main plugin (MatrixSync).

## Hot Reload

By default, the plugin will only start the message exchange process after the game server has finished starting up. After reloading the plugin, the message exchange process will not start automatically.

To start the message exchange process, execute the MCDR command `!!msync`, which can be used both in-game and in the console.

This command does not require any permissions, but it sets up a process lock (a safety mechanism). Repeated execution will trigger a warning prompt, but it will not affect the normal operation of the plugin.

Please note that this feature is experimental. If you encounter any errors, please provide feedback to the plugin author through GitHub Issues!

## Notes
- When the plugin is first loaded, it will automatically initialize the configuration and then unload itself. You need to correctly modify the default configuration file and enable the `plugin_enabled` configuration item in `settings.json` to enable the plugin. After that, restart the server or reload the plugin to use it normally.
- End-to-end encryption (EE2E) is not supported. If needed, you can customize and modify the plugin yourself, or submit a pull request (PR) with your changes.
