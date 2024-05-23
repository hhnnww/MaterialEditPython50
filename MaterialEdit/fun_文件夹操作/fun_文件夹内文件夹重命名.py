from pathlib import Path
from typing import Union
from uuid import uuid1


def fun_文件夹内文件夹重命名(
    material_path: Union[str, Path], shop_name: str, num: int = 1
):
    if isinstance(material_path, str):
        material_path = Path(material_path)

    for in_path in material_path.iterdir():
        if in_path.is_dir():
            in_path.rename(in_path.with_name(str(uuid1())))

    for in_path in material_path.iterdir():
        if in_path.is_dir():
            num_str = str(num)
            while len(num_str) < 2:
                num_str = "0" + num_str

            in_path.rename(in_path.with_name(shop_name + "(" + num_str + ")"))
            num += 1
