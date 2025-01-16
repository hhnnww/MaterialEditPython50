"""桌面文件夹操作."""

from pathlib import Path

from PIL import Image


def fun_保存图片(im: Image.Image, stem: str, material_id: str = "") -> None:
    """保存图片."""
    if im.mode != "RGB":
        im = im.convert("RGB")

    ma_path = Path.home() / "Desktop" / "UPLOAD"

    if ma_path.exists() is False:
        ma_path.mkdir(parents=True)

    if material_id != "":
        jpg_path = ma_path / f"{material_id}-{stem}.jpg"
    else:
        jpg_path = ma_path / f"{stem}.jpg"

    im.save(jpg_path.as_posix(), quality=90)
    im.close()


def fun_清空桌面上传文件夹图片(in_stem: str) -> None:
    """清空桌面上传文件夹图片."""
    ma_path = Path.home() / "Desktop" / "UPLOAD"

    if ma_path.exists() is not True:
        return

    for in_file in ma_path.iterdir():
        if in_stem in in_file.stem:
            in_file.unlink()
