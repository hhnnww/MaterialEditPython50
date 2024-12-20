"""获取素材文件夹所有素材文件的大小."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def get_all_material_file_size(all_file: list[Path]) -> str:
    """获取素材所有尺寸."""
    size: int | float = sum([obj.stat().st_size for obj in all_file])
    size_level = ["bytes", "kb", "mb", "gb"]
    size_unit = 1024
    num = 0

    while size > size_unit:
        size = size / size_unit
        num += 1

    size = round(number=size, ndigits=2)

    return f"{size} {size_level[num].upper()}"
