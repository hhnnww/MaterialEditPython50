"""删除图片透明边框"""

from pathlib import Path

from PIL import Image
from tqdm import tqdm


def fun_删除图片透明边框(image: Image.Image) -> Image.Image:
    """删除图片边框."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    alpha = image.split()[3]
    bbox = alpha.getbbox()

    if bbox:
        image = image.crop(bbox)

    return image


if __name__ == "__main__":
    all_image = [
        infile
        for infile in Path(r"F:\小夕素材\11000-11999\11207\11207").rglob("*")
        if infile.is_file() and infile.suffix.lower() in [".png"]
    ]
    for infile in tqdm(all_image, desc="删除图片透明边框", ncols=100):
        with Image.open(infile.as_posix()) as im:
            fun_删除图片透明边框(im).save(infile.as_posix())
