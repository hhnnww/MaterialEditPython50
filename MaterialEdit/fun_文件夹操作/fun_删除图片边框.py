from pathlib import Path

from PIL import Image, ImageChops


def del_border(im_path: str):
    im = Image.open(im_path)
    im = im.convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()

    if bbox:
        im = im.crop(bbox)
        im = im.convert("RGBA")
        im.save(im_path)


def fun_删除图片边框(material_path: str):
    for png_path in Path(material_path).rglob("*"):
        if png_path.is_file() and png_path.suffix.lower() in [".png"]:
            del_border(png_path.as_posix())
