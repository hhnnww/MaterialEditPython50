from pathlib import Path
from uuid import uuid4

from .fun_遍历指定文件 import fun_遍历指定文件


def fun_子目录PSD重命名(material_path: str):
    # 先改成UUID文件名
    all_file = fun_遍历指定文件(folder=material_path, suffix=[".psd", ".psb"])
    for in_file in all_file:
        in_file: Path
        in_file.rename(in_file.with_stem(str(uuid4())))

    # 所有文件改名
    # all_file = fun_遍历指定文件(folder=material_path, suffix=[".psd", ".psb"])
    # for num, in_file in enumerate(all_file):
    #     in_file: Path
    #     if in_file.parent == Path(material_path):
    #         continue

    #     if num == 0:
    #         new_path = in_file.with_stem(f"{in_file.parent.stem}")
    #     else:
    #         new_path = in_file.with_stem(f"{in_file.parent.stem}-{num}")

    #     in_file.rename(new_path)

    # 子目录
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            all_file = fun_遍历指定文件(
                folder=in_path.as_posix(), suffix=[".psd", ".psb"]
            )

            for num, in_file in enumerate(all_file):
                new_path = in_file.with_stem(f"{in_file.parent.stem}_{num+1}")

                in_file.rename(new_path)
