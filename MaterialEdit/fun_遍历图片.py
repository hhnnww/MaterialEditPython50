from pathlib import Path

from MaterialEdit.fun_获取路径数字 import fun_获取路径数字
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_遍历图片(folder: str, used_image_number: int, image_sort: bool) -> list[str]:
    l = []
    for in_file in Path(folder).rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            l.append(in_file)

    l.sort(key=lambda k: fun_获取路径数字(k.stem), reverse=not image_sort)

    if used_image_number > 0:
        return [obj.as_posix() for obj in l][:used_image_number]

    return [obj.as_posix() for obj in l]
