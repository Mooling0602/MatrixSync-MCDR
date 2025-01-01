from . import *
from typing import Optional


def tr(tr_key: str, return_str: Optional[bool] = True):
    '''
    对`PluginServerInterface.rtr()`进行优化，提高翻译效率。

    参数:
        tr_key (str): 原始或简化后的翻译键名称
        return_str (可选[bool]): 是否尝试转换成字符串减少出错

    返回:
        translation: RTextMCDRTranslation组件
        或tr_to_str: 字符串
    '''
    if tr_key.startswith(f"{plgSelf.id}"):
        translation = psi.rtr(f"{tr_key}")
    else:
        # 使用此前缀代表非本插件的翻译键，则翻译时不会附加本插件的ID，避免错误。
        if tr_key.startswith("#"):
            translation = psi.rtr(tr_key.replace("#", ""))
        else:
            translation = psi.rtr(f"{plgSelf.id}.{tr_key}")
    if return_str:
        tr_to_str: str = str(translation)
        return tr_to_str
    else:
        return translation

__all__ = ["tr"]
import sys
sys.modules[__name__] = tr
