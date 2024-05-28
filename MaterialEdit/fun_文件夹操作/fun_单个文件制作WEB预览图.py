from pathlib import Path

from PIL import Image


def fun_单个文件制作WEB预览图(image_path: Path):
    """
    单个图片制作WEB预览图
    """
    new_path = image_path.with_stem(f"{image_path.stem}_thumb")

    if new_path.exists() is False:
        im = Image.open(image_path.as_posix())
        if im.mode != "RGBA":
            im = im.convert("RGBA")

        im.thumbnail((500, 500))
        im.save(new_path.as_posix())

    return new_path
