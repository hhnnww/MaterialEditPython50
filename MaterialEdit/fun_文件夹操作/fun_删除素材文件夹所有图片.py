from pathlib import Path

from ..setting import IMAGE_SUFFIX


def fun_删除素材文件夹所有图片(folder: str):
    folder_obj = Path(folder)

    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            in_file.unlink()
