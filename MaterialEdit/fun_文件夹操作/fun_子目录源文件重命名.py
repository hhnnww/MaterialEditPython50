"""模块功能: 提供对指定路径下子目录中的源文件进行批量重命名的功能。

主要功能:
1. 遍历指定路径下的所有子目录。
2. 对每个子目录中的源文件进行两步重命名操作:
- 第一步: 使用随机 UUID 和编号对文件进行初步重命名。
- 第二步: 按文件名排序后，重新命名为以子目录名称为前缀的格式。
注意事项:
- 文件重命名操作会覆盖原有文件名，请确保在调用此模块前备份重要数据。
- 函数依赖以下全局变量或函数:
- MATERIAL_SOURCE_SUFFIX: 指定的文件后缀，用于筛选源文件。
- rglob: 遍历目录并返回符合条件的文件路径的函数。
适用场景:
- 批量整理素材文件。
- 统一子目录中源文件的命名规则。
使用方法:
1. 调用 `fun_子目录源文件重命名` 函数，传入包含子目录的主目录路径。
2. 函数会自动对每个子目录中的源文件进行重命名操作。

"""

from pathlib import Path
from uuid import uuid4

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import MATERIAL_SOURCE_SUFFIX


def fun_子目录源文件重命名(material_path: str) -> None:
    """遍历指定路径下的所有子目录，并对每个子目录中的源文件进行重命名操作。

    参数:
        material_path (str): 包含子目录的主目录路径。
    功能:
    1. 对每个子目录中的源文件进行初步重命名，使用随机 UUID 作为文件名。
    2. 对初步重命名后的文件按文件名排序，并重新命名为以子目录名称为前缀的格式。
       - 第一个文件命名为子目录名称。
       - 后续文件命名为子目录名称加编号（如：子目录名称_1, 子目录名称_2）。
    注意:
    - 函数假设 MATERIAL_SOURCE_SUFFIX 和 rglob 是已定义的全局变量或函数。
    - 文件重命名操作会覆盖原有文件名，请确保在调用此函数前备份重要数据。
    """

    def __单个目录重命名(sub_path: Path) -> None:
        uuid = str(uuid4())
        for num, infile in enumerate(
            rglob(folder=sub_path.as_posix(), suffix=MATERIAL_SOURCE_SUFFIX),
        ):
            infile.rename(
                infile.with_stem(f"{uuid}_{num}"),
            )

        all_file = rglob(folder=sub_path.as_posix(), suffix=MATERIAL_SOURCE_SUFFIX)
        all_file.sort(key=lambda k: k.stem)
        for num, infile in enumerate(all_file):
            if num == 0:
                new_path = infile.with_stem(f"{sub_path.stem}")
            else:
                new_path = infile.with_stem(f"{sub_path.stem}_{num}")
            infile.rename(new_path)

    for sub_path in Path(material_path).iterdir():
        if sub_path.is_dir():
            __单个目录重命名(sub_path)


if __name__ == "__main__":
    fun_子目录源文件重命名(material_path=r"F:\小夕素材\11000-11999\11173\11173")
