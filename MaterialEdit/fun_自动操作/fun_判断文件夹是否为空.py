from pathlib import Path


def fun_判断是否为空文件夹(root_path: Path):
    for in_file in root_path.rglob("*"):
        if in_file.is_file():
            return True
    return False
