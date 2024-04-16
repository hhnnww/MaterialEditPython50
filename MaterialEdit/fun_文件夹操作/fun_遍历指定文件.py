from pathlib import Path

from ..fun_获取路径数字 import fun_获取路径数字


def fun_遍历指定文件(folder: str, suffix: list[str]) -> list[Path]:
    folder_obj = Path(folder)
    l = []

    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in suffix:
            l.append(in_file)

    l.sort(key=lambda k: fun_获取路径数字(k.stem))

    return l
