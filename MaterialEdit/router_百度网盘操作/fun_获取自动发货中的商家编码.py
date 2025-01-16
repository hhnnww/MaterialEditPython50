"""获取自动发货中的商家编码."""

import re


def fun_获取自动发货中的商家编码(text: str) -> list[str]:
    """获取自动发货中的商家编码."""
    return re.findall(r"商家编码：(.*?)\n", text)
