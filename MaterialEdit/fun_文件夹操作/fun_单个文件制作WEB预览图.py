"""预览图制作WEB图."""

from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def image_make_web_thumbnail(image_path: Path) -> Path:
    """单个图片制作WEB预览图."""
    if "_thumb" in image_path.stem:
        return image_path

    new_path = image_path.with_stem(f"{image_path.stem}_thumb")
    if new_path.exists() is False:
        with Image.open(image_path.as_posix()) as im:
            max_height_ratio = 5
            if im.height / im.width > max_height_ratio:
                croped_im = im.crop(
                    (0, 0, im.width, int(im.width * (max_height_ratio - 0.1))),
                )
            else:
                croped_im = im

            croped_im.thumbnail((900, 900))
            if im.mode == "CMYK":
                if new_path.suffix.lower() != ".png":
                    croped_im = croped_im.convert("RGB")
                else:
                    croped_im = croped_im.convert("RGBA")

            croped_im.save(new_path.as_posix())

    return new_path
