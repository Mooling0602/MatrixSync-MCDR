- 中文
- English (Unsupported yet, please use translate tools.)

# MatrixSync-MCDR 文档
这里是MCDReforged插件MatrixSync的文档。

插件配置部分仍保留在README。

## 接口（API）
这里介绍插件提供的内部接口。

### 新版接口（v2.4.0）
2.4.0版本以后，插件完善了已有的消息上报器（MC -> Matrix）接口。

简单用法：
```python
import ...
from matrix_sync.reporter import send_matrix

def main():
    # 若message为MCDR.ServerInterface.rtr()，你需要将其转换为str类型，或改用MCDR.ServerInterface.tr()，否则会发生错误。
    # 该问题的产生原因未知，暂时无法解决。
    message = "你要发送的消息"
    send_matrix(message)
```
目前仍无法获取发送结果，但如果主插件在加载时没有成功初始化客户端，你可以通过以下方式获取到相关报错：
```python
import ...
from matrix_sync.reporter import sender

def main():
    response = send_matrix(message)
    if response is not None:
        print(response)
```
> 在MCDR中，常用`server.logger.info`或`psi.logger.info`代替`print`，以进行更标准化的日志格式输出。

### 旧版接口（v2.2-）
旧版接口含有较大缺陷（会阻塞MCDR主线程，消息发不出去等故障情况将导致MCDR卡死），且已不具备实用的应用场景，但仍然可用。
```python
import ...
import asyncio
from matrix_sync.reporter import sendMsg

def main():
    message = "你要发送的消息"
    asyncio.run(sendMsg(message))

# 或者使用协程，如果你的插件会用到的话
async def async_main():
    message = "你要发送的消息"
    await sendMsg(message)
```
如果你的插件会使用独立的线程运行相关任务，则旧版接口仍然稳定有效。

### 废弃接口（v2.3.x）
即新版接口中这一部分：`from matrix_sync.reporter import send_matrix`，v2.3.x时曾为`sender()`，后发现和派发的Matrix消息事件中的`sender`（Matrix消息发送者）冲突，因此无法兼容，故废弃。

任何情况下，都不要再尝试使用这个接口！

另外，建议停止使用v2.3.x版本。