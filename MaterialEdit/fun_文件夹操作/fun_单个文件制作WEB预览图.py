"""预览图制作WEB图."""

from pathlib import Path

from PIL import Image


def image_make_web_thumbnail(image_path: Path) -> Path:
    """单个图片制作WEB预览图."""
    if "_thumb" in image_path.stem:
        return image_path

    new_path = image_path.with_stem(f"{image_path.stem}_thumb")

    if new_path.exists() is False:
        im = Image.open(image_path.as_posix())
        max_height_ratio = 5
        if im.height / im.width > max_height_ratio:
            im = im.crop((0, 0, im.width, im.width * 5))

        im.thumbnail((500, 500))
        if im.mode == "CMYK":
            if new_path.suffix.lower() != ".png":
                im = im.convert("RGB")
            else:
                im = im.convert("RGBA")

        im.save(new_path.as_posix())

    return new_path
