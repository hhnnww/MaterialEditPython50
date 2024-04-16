import os
from pathlib import Path


def fun_打开所有子文件夹(material_path: str):
    material_path_obj = Path(material_path)

    for in_path in material_path_obj.iterdir():
        if in_path.is_dir():
            os.startfile(in_path.absolute().as_posix())


def fun_是否包含子文件夹(item_path: Path):
    for in_path in item_path.iterdir():
        if in_path.is_dir():
            return True

    return False
