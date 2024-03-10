# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和线上游戏之间的消息。

关于[Matrix](https://matrix.org/)：一个开放的去中心化的网络通讯协议，用于聊天软件。

开发过程中使用了pypi中的项目[matrix-nio](https://pypi.org/project/matrix-nio/)。

当前已完成预览开发版本，支持线上游戏的消息上报到群组中，详情可以先看看issue。

## 用法
从Release下载最新版本，甩到plugins文件夹或你设置的存放插件的文件夹内，然后注意控制台输出的提示即可。

## 注意
- 首次加载插件会初始化配置并自动卸载插件，你需要修改完默认配置后，重启服务器或重载插件才能正常使用。
- 不打算支持加密信息（EE2E），有需要自行修改。
- i18n将在正式版本（v1.1.0）以后得到支持。
- 房间消息转发到游戏内的功能还在开发，由于看不懂文档，可能还需要很长时间。
- For English(and other languages) users, you need to use translate tools at present.
