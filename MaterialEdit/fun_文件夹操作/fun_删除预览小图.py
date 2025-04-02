"""删除预览图文件夹的小图片"""

from MaterialEdit.fun_遍历图片 import fun_遍历图片


def fun_删除预览小图(preview_path: str) -> None:
    """fun_删除预览小图"""
    for in_file in fun_遍历图片(
        folder=preview_path,
        used_image_number=0,
        image_sort=False,
    ):
        if "_thumb" in in_file.stem:
            in_file.unlink()
