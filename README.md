- 中文
- English

# MatrixSync-MCDR
A MCDR (full name [MCDReforged](https://mcdreforged.com/)) plugin, use to sync messages between Matrix groups and online gaming in Minecraft servers.

About [Matrix](https://matrix.org/): an open decentralized network communication protocol for chat software.

The following project is used in the development process: [matrix-nio](https://pypi.org/project/matrix-nio/)。

## Usage
Download the latest version in release, put it in the plugins folder, then follow the prompts in the plugin output in the console to modify the configuration file and reload the plugin, until test message 
is successfully sent to the matrix groups and message-sync will start working.
Before you using this plugin, you must know what [Matrix] is, and prepare an account to use to be a matrix bot for sync messages. In the config, "user" actually means the bot.

## Attention
- The first time you load this plugin, it will init the config and automatically unload itself. You need to modify the default config correctly, restart the server or reload the plugin to use it normally.
- There's no any plans to support encrypted messages(EE2E), if you need you should modify this plugins by yourself.
- I18n currently only support Chinese(Simplified) and English(translated from Chinese with Google Translate), everyone can help with traslations and contact me.
- About room-message receiver, please see the following section.

## Matrix Room-message receiver
It's easy to forward in-game messages to the matrix rooms by listening MCDR Event "User Info", and plugin is designed to forward the obtained game messages to the specified matrix room when listening to this event.
However, to forward messages in the matrix room to the game, there's no listenable event that can be used directly. So the plugins uses an async func to run a loop event for receiving messages from matrix rooms.
During the development process, the content about this part in the matrix-nio documention is obscure and difficult to understand for me.
Currently, the plugin can send game messages to specified matrix rooms, but cannot specify which matrix rooms to receive chat messages from. When forwarding a game message to the matrix room, echo messages will be generated and finally forwarded back to the game.
**To fix the "echo messages" problem, a temporary solution was used in v1.0.1+, and you have to set the bot's display name in the config.** It's possible to get the display name directly using the API provided by matrix-nio, but I find it difficult to understand their documention. I'll improve this after I get it.
Anyway, this feature is fuctional now, but there are still a lot of issues.
It would be great if someone would like to help improve this program.
