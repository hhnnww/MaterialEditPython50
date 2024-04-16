from pathlib import Path
from typing import Optional

from PIL import Image


def fun_保存图片(im: Image.Image, stem: str, material_id: Optional[str] = None):
    if im.mode != "RGB":
        im = im.convert("RGB")

    ma_path = Path.home() / "Desktop" / "UPLOAD"
    if material_id is not None:
        ma_path = Path.home() / "Desktop" / "UPLOAD" / material_id

    if ma_path.exists() is False:
        ma_path.mkdir(parents=True)

    jpg_path = ma_path / (stem + ".jpg")
    im.save(jpg_path.as_posix(), quality=90)
    im.close()


def fun_清空桌面上传文件夹图片(in_stem: str):
    ma_path = Path.home() / "Desktop" / "UPLOAD"

    if ma_path.exists() is not True:
        return

    for in_file in ma_path.iterdir():
        if in_stem in in_file.stem:
            in_file.unlink()
