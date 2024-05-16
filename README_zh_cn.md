- 中文
- [English](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README.md)

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

## 用法
从release下载最新版本，扔到plugins文件夹里面，然后按控制台输出修改配置文件并重载插件，直到测试消息成功发送到matrix群组，消息同步开始工作。

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步。在配置文件中，"user"（“用户”）实际上意为"bot"（“机器人”）。

## 注意
- 首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，然后重启服务器或着重载插件以正常使用。
- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件。
- 多语言目前只支持中文（简体）和英语（用谷歌从中文翻译），任何人都可以联系我帮助翻译。
- 为修复“回音消息”问题，在v1.0.1+版本使用了一个临时的解决方案，你需要在配置文件的"user_name"项中设置机器人账号的显示名称。