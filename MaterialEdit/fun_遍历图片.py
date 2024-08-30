from pathlib import Path

from MaterialEdit.fun_获取路径数字 import fun_获取路径数字
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_遍历图片(folder: str, used_image_number: int, image_sort: bool) -> list[str]:
    image_list = []
    for in_file in Path(folder).rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            image_list.append(in_file)

    image_list.sort(key=lambda k: fun_获取路径数字(k.stem), reverse=not image_sort)

    if used_image_number > 0:
        return [obj.as_posix() for obj in image_list][: used_image_number * 2]

    return [obj.as_posix() for obj in image_list]
