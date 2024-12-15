- [中文](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README.md)
- English
> To avoid incorrect links after merging into the main branch, all URLs should use the main branch's address. If you are accessing other branches, please make sure to manually adjust the link's target location.

# MatrixSync-MCDR
A MCDR (full name [MCDReforged](https://mcdreforged.com/)) plugin, use to sync messages between Matrix groups and online gaming in Minecraft servers.

About [Matrix](https://matrix.org/): an open decentralized network communication protocol for chat software.

The following project is used in the development process: [matrix-nio](https://pypi.org/project/matrix-nio/)。

Thanks for ChatGPT and Google Translate's help to translate the content from Chinese, if anything wrong, please issue to feedback or PR to `/lang`.

## Usage
Download the latest version from the release, install the necessary Python dependencies in the MCDReforged startup environment, and then throw it into the plugins folder.

Before using this plugin, you must know what [Matrix](https://matrix.org/) is, then prepare an account as a matrix bot for message synchronization, and carefully read the following content to configure the plugin.

After configuration and enabling the plugin, if the test message is successfully sent to the matrix group, it means that message synchronization has started to work.

If there is any issue with message forwarding in any direction during the message synchronization process, please check the configuration according to the following content to ensure it is correct.

### Configuration File
#### config.json

| Configuration Item | Content |
| - | - |
| **homeserver** | The homeserver address used to log in to the bot account |
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
See the docs in [中文文档](https://github.com/Mooling0602/MatrixSync-MCDR/blob/docs.md) at present.

## Hot Reload (reload) & message sync control
It is advisable not to use hot reload in a stable environment.

Execute `!!msync` to see the usage.

## Note
### First-time Use
When loading the plugin for the first time, the plugin will automatically initialize the configuration and then unload itself. You need to correctly modify the default configuration file and enable the plugin_enabled option in settings.json to activate the plugin. Then, restart the server or reload the plugin for proper use. If you choose the latter, after reloading the plugin, if the server has finished starting, you can use !!msync start to start the room message receiver, enabling Matrix message forwarding to the game. Furthermore, as long as the plugin is successfully loaded without issues, in-game messages will always be automatically forwarded to the Matrix room. This will be synchronized with the room message receiver in versions above 2.4.0.

- The plugin does not support encrypted messages (EE2E). If needed, you can modify the plugin for secondary development, and PRs are welcome.
