- 中文
- [English](README_en_us.md)

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

> 注意：不再支持`mcdreforged<2.14`

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的pypi项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

版本进度：`v2.5.0`

关于子包（扩展功能支持）请查看此源码仓库：https://github.com/Mooling0602/MSyncSubpacks

## 用法
从release下载最新版本，在MCDReforged的启动环境中安装好需要的Python依赖，然后扔到plugins文件夹里面即可。

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步，并认真阅读下面的内容以进行插件配置。

配置完毕并加载插件后，若有测试消息成功发送到matrix群组，则表示消息同步开始工作。

若消息同步的过程中有任意方向的消息转发出现问题，也请按配置文件部分的内容检查配置是否正确。

### 配置文件
#### config.json

| 配置项 | 配置内容 |
| - | - |
| **homeserver** | 机器人账号所属的根服务器 |
| **user_id** | 机器人的账号ID，格式为@<用户名>:<根服务器>，如@mcchatbot:example.com |
| **password** | 机器人账号的密码，在初次登录和重新生成token时使用 |
| **room_id** | 需要同步游戏消息的房间的ID，使用管理员权限在房间设置中查看 |
| **device_id** | 登录用的设备名，一般无需修改，可自定义 |

> 只支持单账号和单聊天房间（相当于QQ群），计划在v3版本以后开发多配置管理。
> 
> v2 LTS 开发中，如果你不需要多账号、多房间管理，可以持续使用v2版本。
> 
> v2 LTS 推送正在进行，配置文件格式已大幅度修改，可能和之前完全不兼容，建议备份后删除旧配置并按照新的配置格式重新设置插件。

#### settings.json

| 配置项 | 配置内容 |
| - | - |
| `listen.all_rooms` | 是否接收来自机器人加入的所有房间的消息，默认全部接收 |
| `listen.old_messages` | 是否在启动接收器时加载历史消息，默认不加载 |
| `message_format.single_room` | 只接收当前配置的房间的消息时，消息的显示格式 |
| `message_format.all_room` | 接收机器人加入的所有房间的消息时，消息的显示格式 |
| `log_style.mcdr` | 是否使用MCDR的日志样式，默认为否（使用插件自己的日志样式） |
| `log_style.debug` | 是否显示调试日志，默认为否 |
| `ver` | 配置文件版本，请不要进行修改 |

## 接口（API）
请前往[docs](https://github.com/Mooling0602/MatrixSync-MCDR/blob/dev/docs.md)查看。

v2.5.0进行了一次彻底的代码重构，并且此版本开始进行长期支持，此前的所有API全部失效，并且此前的配置文件不再受支持。

## 热重载（reload）及消息互通控制
始终建议在运行环境稳定时，尽量不使用热重载，减少出错概率

插件加载时会自动启动消息接收器（转发Matrix消息到MCDR控制台，被动），游戏内的玩家聊天也会自动转发到Matrix（主动），目前前者可以手动进行开关。

插件卸载时或停止消息接收器时，会自动关闭消息接收器，并关闭运行中的异步客户端。

若出现插件卸载后仍有残留线程运行的情况，请反馈到Issues页面。遇到这种情况，你只能完全退出甚至强制退出MCDR。
> 目前这个问题基本不会发生，但不排除有没考虑到的情况。一般情况下，你可以随意热重载以刷新插件配置。

## 注意
### 关于首次使用
首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，然后重载插件以正常使用。

如果`/path/to/mcdr/config/matrix_sync/config.json`中的机器人账号信息有误，会出现报错，在反馈报错到Issues前，请确认你的信息准确无误，否则无助于解决问题。

- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件，欢迎PR。

- 多语言目前只支持中文（简体）和英语（用谷歌和ChatGPT从中文翻译），任何人都可以联系我帮助完善翻译，欢迎PR到/lang语言文件和README中。
