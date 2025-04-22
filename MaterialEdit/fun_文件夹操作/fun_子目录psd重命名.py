"""文件重命名.py"""

from pathlib import Path
from uuid import uuid4

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


def fun_子目录PSD重命名(material_path: str) -> None:
    """子目录PSD重命名."""
    # 先改成UUID文件名
    all_file = rglob(folder=material_path, suffix=[".psd", ".psb"])
    for in_file in all_file:
        in_file: Path
        in_file.rename(in_file.with_stem(str(uuid4())))

    # 子目录
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            all_file = rglob(
                folder=in_path.as_posix(),
                suffix=[".psd", ".psb"],
            )

            for num, in_file in enumerate(all_file):
                if num == 0:
                    new_path = in_file.with_stem(f"{in_file.parent.stem}")
                else:
                    new_path = in_file.with_stem(f"{in_file.parent.stem}_{num}")

                in_file.rename(new_path)
