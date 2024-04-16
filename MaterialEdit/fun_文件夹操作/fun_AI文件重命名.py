from pathlib import Path

from .fun_遍历指定文件 import fun_遍历指定文件
from uuid import uuid4


def fun_ai文件重命名(material_path: str):
    ai_file_list = fun_遍历指定文件(folder=material_path, suffix=[".ai", ".eps", ".pptx"])

    for in_file in ai_file_list:
        if in_file.parent != Path(material_path):
            in_file = in_file.rename(in_file.with_stem(str(uuid4())))

            new_name = in_file.with_stem(f"{in_file.parent.stem}")

            x = 1
            while new_name.exists() is True:
                new_name = in_file.with_stem(f"{in_file.parent.stem}_{x}")
                x += 1

            in_file.rename(new_name)
