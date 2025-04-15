"""预览图制作WEB图."""

from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def image_make_web_thumbnail(image_path: Path) -> Path:
    """单个图片制作WEB预览图."""
    if "_thumb" in image_path.stem:
        return image_path

    new_path = image_path.with_stem(f"{image_path.stem}_thumb")
    max_size = 20
    if (
        new_path.exists() is False
        and image_path.stat().st_size / 1000 / 1000 < max_size
    ):
        with Image.open(image_path.as_posix()) as im:
            max_height_ratio = 10
            if im.height / im.width > max_height_ratio:
                im = im.crop((0, 0, im.width, im.width * 9))

            im.thumbnail((500, 500))
            if im.mode == "CMYK":
                if new_path.suffix.lower() != ".png":
                    im = im.convert("RGB")
                else:
                    im = im.convert("RGBA")

            im.save(new_path.as_posix())

    return new_path
