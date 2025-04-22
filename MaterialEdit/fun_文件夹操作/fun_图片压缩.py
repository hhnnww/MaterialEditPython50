"""压缩图片"""

from pathlib import Path

from PIL import Image
from tqdm import tqdm

from MaterialEdit.setting import IMAGE_SUFFIX


def fun_图片压缩(material_path: str) -> None:
    """压缩指定文件夹中超过最大大小的图片文件 并将其保存为JPEG格式。"""
    max_size = 20
    for infile in tqdm(
        [
            infile
            for infile in Path(material_path).rglob("*")
            if infile.is_file()
            and infile.parent.stem.lower() != "links"
            and infile.suffix.lower() in IMAGE_SUFFIX
            and infile.stat().st_size / 1000 / 1000 > max_size
        ],
        desc="压缩图片",
        unit="个",
        ncols=100,
    ):
        with Image.open(infile.as_posix()) as im:
            save_path = infile.with_suffix(".jpg")
            im.convert("RGB").save(save_path.as_posix(), quality=60, subsampling=0)

        if infile.suffix.lower() == ".png":
            infile.unlink()
