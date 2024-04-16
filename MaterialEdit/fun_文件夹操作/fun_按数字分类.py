import math
import re
from pathlib import Path


def fun_按数字分类(material_path: str):
    material_path_obj = Path(material_path)

    for in_file in material_path_obj.rglob("*"):
        if in_file.is_file():
            path_stem_num = fun_获取文件中的NUM(in_file.stem)

            if path_stem_num is None:
                continue

            num_parent_path = material_path_obj / fun_根据数字计算对应文件夹(path_stem_num)

            if in_file.parent != num_parent_path:
                new_path = num_parent_path / in_file.name

                if num_parent_path.exists() is False:
                    num_parent_path.mkdir()

                in_file.rename(new_path.as_posix())


def fun_获取文件中的NUM(path_stem: str):
    num = re.findall(r"\((\d+)\)", path_stem)
    if len(num) > 0:
        return int(num[0])

    return None


def fun_根据数字计算对应文件夹(num: int):
    start_num = str(math.floor(num / 100)) + "00"
    end_num = str(math.floor(num / 100)) + "99"

    return start_num + "-" + end_num
