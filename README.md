- 中文
- [English](https://github.com/Mooling0602/MatrixSync-MCDR/blob/README_en_us.md)

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的pypi项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

当前分支版本：主分支@2.4.0

## 用法
从release下载最新版本，在MCDReforged的启动环境中安装好需要的Python依赖，然后扔到plugins文件夹里面即可。

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步，并认真阅读下面的内容以进行插件配置。

配置完毕并启用插件后，若有测试消息成功发送到matrix群组，则表示消息同步开始工作。

若消息同步的过程中有任意方向的消息转发出现问题，也请按配置文件部分的内容检查配置是否正确。

### 使用 Git 从源码打包插件
> This part doesn't support English yet, please use translate tools at present.
> 
> 依赖软件包`zip`
> 
> 在终端上运行`git clone https://github.com/Mooling0602/MatrixSync-MCDR.git`，然后进入`MatrixSync-MCDR`目录下并运行`pack_plugin.sh`（记得给文件设置可执行权限）
>
> 若无法正常访问GitHub，可以运行`git clone https://mirror.ghproxy.com/https://github.com/Mooling0602/MatrixSync-MCDR.git`
>
> 懒人用命令：`git clone https://mirror.ghproxy.com/https://github.com/Mooling0602/MatrixSync-MCDR.git && cd MatrixSync-MCDR && chmod +x pack_plugin.sh && ./pack_plugin.sh`
>
> 打包脚本所用配置（config.ini）中的ci部分为主插件和配套子包的构建开关，设置为1即可打开，脚本运行后将生成打包好的插件，其中子包的构建在`subpack(rolling)/[MSync]*/内（如果开发完成），主插件的构建在主目录。

### 配置文件
#### config.json

| 配置项 | 配置内容 |
| - | - |
| **homeserver** | 机器人账号登录所使用的根服务器 |
| **user_id** | 机器人的账号ID，格式为@<用户名>:<根服务器>，如@mcchatbot:example.com |
| **password** | 机器人账号的密码，仅在初次登录使用 |
| **room_id** | 需要接收游戏消息的房间的ID |
| **room_name** | 需要转发消息到游戏内的房间的显示名称（必须准确无误，若发生更新也需要同步修改，否则你将看不到任何消息） |
| **device_id** | 登录用的设备名，一般无需修改，可自定义 |

> 目前只支持单账号和单聊天房间（相当于QQ群），计划在v3版本以后开放多配置接口支持。

#### settings.json

| 配置项 | 配置内容 |
| - | - |
| plugin-enabled | 插件是否启用，请确保配置文件和所需设置修改无误后再开启 |
| allow_all_rooms_msg | 是否允许来自所有房间的消息，若开启，则来自机器人账号所加入的房间的消息都会被转发到游戏中，并注明房间的显示名称，否则只转发已设置的房间的消息 |
| sync_old_msg | 是否同步旧的消息，默认关闭，开启以在插件启动同步时加载历史消息 |

## 接口（API）
2.3.0以前的旧接口仍然有效，请到[docs](https://github.com/Mooling0602/MatrixSync-MCDR/blob/dev/docs.md)查看。

> 2.3.x修改的接口将不再受到任何支持，原因为相关函数名和分发的插件事件中提供的参数发生冲突。

2.4.0版本重构后的新接口的简单用法：
```python
import matrix_sync.client
from matrix_sync.reporter import send_matrix

def main():
    message = "你要发送的消息"
    clientStatus = matrix_sync.client.clientStatus
    if clientStatus:
        send_matrix(message)

# 消息将在独立线程MatrixReporter中被发送到Matrix，不再可能会阻塞MCDR主线程
```

## 热重载（reload）及消息互通控制
插件默认在游戏服务端启动完成时自动启动房间消息接收进程，在游戏服务端关闭后自动关闭房间消息接收进程。

要手动启动房间消息接收器（例如重载插件后的场景），请执行MCDR命令`!!msync start`，游戏内和控制台上都可以使用。

要提前关闭房间消息接收器，可以在控制台使用`!!msync stop`，直到下次服务器启动完成前消息接收器都必须手动使用`!!msync start`重新启动。

插件会自动在解析到游戏内的消息时尝试转发到配置好的Matrix房间内，暂时无法禁用，将于v2.4.0以后版本（v2.4.x）中通过和房间消息接收器同步开闭状态的方式解决。

该指令没有权限要求，但设置了进程锁（安全机制），重复执行会警告提示，不会影响插件功能的正常运行。

请注意，该功能仍然是不稳定的，若发现任何错误请及时通过GitHub Issue向插件作者反馈。另外，重载插件前尽量先关闭房间消息接收器，否则可能无法清楚残留进程，导致只能重启整个MCDR解决！

建议在运行环境稳定时，尽量不使用热重载。

## 注意
### 关于首次使用
首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，并在settings.json中启用plugin_enabled配置项以启用插件，然后重启服务器或着重载插件以正常使用。若选择后一个方案，在插件重载后如果服务器已启动完毕，你可以使用`!!msync start`启动房间消息接收器，使Matrix的消息转发到游戏内。另外，只要插件成功加载没有出现问题，游戏内的消息将始终自动转发到Matrix的房间，将在v2.4.0以上版本中改为和房间消息接收器同步。

- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件，欢迎PR。

- 多语言目前只支持中文（简体）和英语（用谷歌和ChatGPT从中文翻译），任何人都可以联系我帮助完善翻译，欢迎PR到/lang语言文件和README中。
