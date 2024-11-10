- [中文](https://github.com/Mooling0602/MatrixSync-MCDR/blob/dev/README.md)
- English

# MatrixSync-MCDR
A MCDR (full name [MCDReforged](https://mcdreforged.com/)) plugin, use to sync messages between Matrix groups and online gaming in Minecraft servers.

About [Matrix](https://matrix.org/): an open decentralized network communication protocol for chat software.

The following project is used in the development process: [matrix-nio](https://pypi.org/project/matrix-nio/)。

Thanks for ChatGPT and Google Translate's help to translate the content from Chinese, if anything wrong, please issue to feedback or PR to `/lang`.

Present branch version: dev@2.4.0

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
| **room_id** | The ID of the room to receive game messages |
| **room_name** | The display name of the room to forward messages to the game (must be accurate, if updated, it also needs to be modified synchronously, otherwise you will not see any messages) |
| **device_id** | The device name used for login, generally no need to modify, can be customized |

Multi-config is not supported, will add API support for developers from v3.
#### settings.json

| Configuration Item | Content |
| - | - |
| plugin-enabled | Whether the plugin is enabled, please ensure the configuration file and necessary settings are modified correctly before enabling |
| allow_all_rooms_msg | Whether to allow messages from all rooms, if enabled, messages from rooms joined by the bot account will be forwarded to the game, with the room display name specified, otherwise only messages from the configured room will be forwarded |
| sync_old_msg | Whether to sync old messages, enabled on default, disable to see old messages when plugin is just loaded |

## Interface (API)
See "接口（API）" [中文](https://github.com/Mooling0602/MatrixSync-MCDR/blob/dev/README.md) README.

## Hot Reload (reload) & message sync control
By default, the plugin automatically starts the room message reception process when the game server starts and automatically stops the process when the game server shuts down.

To manually start the room message receiver (e.g., after reloading the plugin), execute the MCDR command !!msync start, which can be used both in-game and in the console.

To stop the room message receiver in advance, you can use !!msync stop in the console. The message receiver must be manually restarted with !!msync start before the next server startup.

The plugin will automatically attempt to forward in-game messages to the configured Matrix room when parsing them. This feature cannot be disabled at the moment but will be resolved in version 2.4.0 (v2.4.x) by syncing the open/close status with the room message receiver.

This command has no permission requirements but is protected by a process lock (security mechanism). Repeated execution will trigger a warning but will not affect the normal operation of the plugin.

Please note that this feature is still unstable. If any errors occur, please report them promptly via GitHub Issues to the plugin author. Additionally, before reloading the plugin, it's recommended to close the room message receiver, as failing to do so may leave residual processes that could only be cleared by restarting the entire MCDR.

It is advisable not to use hot reload in a stable environment.

## Note
### First-time Use
When loading the plugin for the first time, the plugin will automatically initialize the configuration and then unload itself. You need to correctly modify the default configuration file and enable the plugin_enabled option in settings.json to activate the plugin. Then, restart the server or reload the plugin for proper use. If you choose the latter, after reloading the plugin, if the server has finished starting, you can use !!msync start to start the room message receiver, enabling Matrix message forwarding to the game. Furthermore, as long as the plugin is successfully loaded without issues, in-game messages will always be automatically forwarded to the Matrix room. This will be synchronized with the room message receiver in versions above 2.4.0.

- The plugin does not support encrypted messages (EE2E). If needed, you can modify the plugin for secondary development, and PRs are welcome.