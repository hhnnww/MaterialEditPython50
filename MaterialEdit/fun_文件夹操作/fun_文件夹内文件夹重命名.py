"""重命名指定文件夹内的所有子文件夹，先随机命名再按指定格式命名。"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid1


def fun_文件夹内文件夹重命名(
    material_path: str | Path,
    shop_name: str,
    num: int = 1,
) -> None:
    """重命名指定文件夹内的所有子文件夹，先随机命名再按指定格式命名。"""
    if isinstance(material_path, str):
        material_path = Path(material_path)

    for in_path in material_path.iterdir():
        if in_path.is_dir():
            in_path.rename(in_path.with_name(str(uuid1())))

    num_count = 2
    for in_path in material_path.iterdir():
        if in_path.is_dir():
            num_str = str(num)
            while len(num_str) < num_count:
                num_str = "0" + num_str

            in_path.rename(in_path.with_name(shop_name + "(" + num_str + ")"))
            num += 1
