- 中文
- English (Unsupported yet, please use translate tools.)

# MatrixSync-MCDR 文档
这里是MCDReforged插件MatrixSync的文档。

插件配置部分仍保留在README。

## 接口（API）
这里介绍插件提供的内部接口。

### 新版接口（v2.3.2）
2.3版本以后，插件开始重构已有的消息上报器（MC -> Matrix）接口，至2.3.2完善。

简单用法：
```python
import ...
from matrix_sync.reporter import sender

def main():
    sender(message)
```
目前仍无法获取发送结果，但如果主插件在加载时没有成功初始化客户端，你可以通过以下方式获取到相关报错：
```python
import ...
from matrix_sync.reporter import sender

def main():
    response = sender(message)
    if response is not None:
        print(response)
```
> 在MCDR中，常用`server.logger.info`或`psi.logger.info`代替`print`，以进行更标准化的日志格式输出。

### 旧版接口（v2.3-）
旧版接口含有较大缺陷，且已不具备实用的应用场景，但仍然可用，后续有空再补充。
