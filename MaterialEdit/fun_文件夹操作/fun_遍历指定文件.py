"""遍历文件夹下的所有制定类型文件."""

from pathlib import Path

from MaterialEdit.get_stem_num import get_path_num


def rglob(folder: str, suffix: list[str]) -> list[Path]:
    """递归遍历文件夹下的所有文件."""
    folder_obj = Path(folder)

    image_list = [
        in_file
        for in_file in folder_obj.rglob("*")
        if in_file.is_file() and in_file.suffix.lower() in suffix
    ]

    image_list.sort(key=lambda k: get_path_num(stem=k.stem))

    return image_list
