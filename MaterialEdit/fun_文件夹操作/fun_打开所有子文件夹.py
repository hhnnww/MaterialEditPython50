"""打开享设计素材所有子文件夹."""

import subprocess
from pathlib import Path


def open_sub_path(material_path: str) -> None:
    """打开享设计类的素材所有子文件夹."""
    material_path_obj = Path(material_path)

    for in_path in material_path_obj.iterdir():
        abso_path = f"C:/Windows/explorer.exe {in_path.absolute().as_posix()}"
        subprocess.Popen(abso_path)


def has_sub_path(item_path: Path) -> bool:
    """判断是否包含子文件夹."""
    return any(in_path.is_dir() for in_path in item_path.iterdir())
