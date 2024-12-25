"""遍历文件夹图片."""

from pathlib import Path

from MaterialEdit.get_stem_num import get_path_num
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_遍历图片(folder: str, used_image_number: int, image_sort: bool) -> list[str]:  # noqa: FBT001
    """遍历文件夹图片."""
    image_list = [
        in_file for in_file in Path(folder).rglob("*") if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX
    ]
    image_list.sort(key=lambda k: get_path_num(k.stem), reverse=not image_sort)
    if used_image_number > 0:
        return [obj.as_posix() for obj in image_list][: used_image_number * 2]
    return [obj.as_posix() for obj in image_list]
