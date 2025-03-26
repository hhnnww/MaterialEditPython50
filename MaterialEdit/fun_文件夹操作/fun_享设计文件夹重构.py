"""模块功能: 享设计文件夹重构。

提供用于重构设计文件夹的功能，包括删除特定类型的文件、移动文件到子文件夹以及清理空文件夹。
包含的函数:
1. fun_享设计文件夹重构(material_path: str) -> None:
    - 遍历指定路径下的所有子文件夹，
    并对每个子文件夹调用 `fun_单个文件夹重构` 函数进行重构操作。
    - 参数:
        - material_path (str): 设计文件夹的路径。
    - 返回:
        - None
2. fun_单个文件夹重构(in_material_path: Path) -> None:
    - 对指定文件夹中的文件进行以下操作：
        1. 删除所有字体文件，扩展名为 .otf, .ttf, .woff, .woff2。
    - 参数:
        - in_material_path (Path): 要重构的文件夹路径。
    - 注意:
"""

from pathlib import Path


def fun_享设计文件夹重构(material_path: str) -> None:
    """重构指定路径下的设计文件夹。

    此函数会遍历给定路径下的所有子文件夹
    并对每个子文件夹调用 `fun_单个文件夹重构` 函数进行重构操作。
    参数:
        material_path (str): 设计文件夹的路径。
    返回:
        None
    """
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            fun_单个文件夹重构(in_material_path=in_path)


def fun_单个文件夹重构(in_material_path: Path) -> None:
    """重构指定文件夹的内容。

    此函数会对指定文件夹中的文件进行以下操作：
    1. 删除所有字体文件 扩展名为 .otf, .ttf, .woff, .woff2。
    2. 将非 .ai 和 .eps 文件移动到子文件夹 "Links" 中。
    3. 删除所有空文件夹。
    参数:
        in_material_path (Path): 要重构的文件夹路径。
    注意:
        - 此函数会直接修改文件系统，删除或移动文件时请小心操作。
        - 如果文件夹中存在同名文件，移动操作可能会失败。
    """
    links_path = in_material_path / "Links"

    for in_file in in_material_path.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() not in [".ai", ".eps"]:
            if in_file.suffix.lower() in [".otf", ".ttf", ".woff", ".woff2"]:
                in_file.unlink()
            else:
                if links_path.exists() is False:
                    links_path.mkdir()
                new_path = links_path / in_file.name
                if new_path.exists() is False:
                    in_file.rename(new_path)

    for in_path in in_material_path.iterdir():
        if in_path.is_dir() and len(list(in_path.iterdir())) == 0:
            in_path.unlink(missing_ok=True)


if __name__ == "__main__":
    fun_单个文件夹重构(Path(r"E:\小夕素材\10000-20000\10250\10250\小夕素材(02)"))
