"""获取素材文件夹所有素材文件的大小"""

from pathlib import Path
from typing import Union


def fun_获取所有尺寸(all_file: list[Path]):
    """获取素材所有尺寸"""
    size: Union[int, float] = sum([obj.stat().st_size for obj in all_file])
    size_level = ["bytes", "kb", "mb", "gb"]

    num = 0
    while size > 1024:
        size = size / 1024
        num += 1

    size = round(size, 2)

    return f"{size} {size_level[num].upper()}"
