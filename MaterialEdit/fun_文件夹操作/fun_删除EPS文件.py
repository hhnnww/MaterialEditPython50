"""删除EPS文件"""

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


def fun_删除EPS文件(material_path: str) -> None:
    """删除EPS文件。"""
    eps_file_list = rglob(folder=material_path, suffix=[".eps"])
    for eps_file in eps_file_list:
        eps_file.unlink()
