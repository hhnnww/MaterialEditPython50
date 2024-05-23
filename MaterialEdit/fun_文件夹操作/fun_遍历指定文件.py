from pathlib import Path

from ..fun_获取路径数字 import fun_获取路径数字


def fun_遍历指定文件(folder: str, suffix: list[str]) -> list[Path]:
    folder_obj = Path(folder)
    image_list = []

    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in suffix:
            image_list.append(in_file)

    image_list.sort(key=lambda k: fun_获取路径数字(k.stem))

    return image_list
