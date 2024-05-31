- 中文
- [English](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README_en_us.md)

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

## 用法
从release下载最新版本，在MCDReforged的启动环境中安装好需要的Python依赖，然后扔到plugins文件夹里面即可。

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步，并认真阅读下面的内容以进行插件配置。

配置完毕并启用插件后，若有测试消息成功发送到matrix群组，则表示消息同步开始工作。

若消息同步的过程中有任意方向的消息转发出现问题，也请按下面的内容检查配置是否正确。

### 配置文件
#### config.json

| 配置项 | 配置内容 |
| - | - |
| **homeserver** | 机器人账号登录所使用的根服务器 |
| **user_id** | 机器人的账号ID，格式为@<用户名>:<根服务器>，如@mcchatbot:example.com |
| **password** | 机器人账号的密码，一般仅在初次登录使用 |
| **room_id** | 需要接收游戏消息的房间的ID，目前只能设置一个 |
| **room_name** | 需要转发消息到游戏内的房间的显示名称（必须准确无误，若发生更新也需要同步修改，否则你将可能看不到任何消息），目前只能设置一个 |

#### settings.json

| 配置项 | 配置内容 |
| - | - |
| plugin-enabled | 插件是否启用，请确保配置文件和所需设置修改无误后再开启 |
| allow_all_rooms_msg | 是否允许来自所有房间的消息，若开启，则来自机器人账号所加入的房间的消息都会被转发到游戏中，并注明房间的显示名称，否则只转发已设置的房间的消息 |
| use_token | 是否使用Token，默认启用，下次重启服务器时会加载部分之前收到的消息（发生在服务器启动完毕时，如果玩家登录过快，可能会在线上游戏内看到），并使用之前的会话继续转发来自Matrix的消息到游戏中；如果不想加载历史消息可以关闭，但每次重启服务器都会产生新的登录会话记录 |

## 注意
- 插件不支持热重载，为确保功能正常，如果尝试重载或者插件，将导致服务器和MCDR直接关闭。
- 首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，然后重启服务器或着重载插件以正常使用。
- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件。
- 多语言目前只支持中文（简体）和英语（用谷歌从中文翻译），任何人都可以联系我帮助翻译。
