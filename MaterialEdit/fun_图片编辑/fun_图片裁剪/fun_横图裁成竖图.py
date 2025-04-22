import math

from PIL import Image

from MaterialEdit.type import ALIGNITEM


def fun_横图裁成竖图(
    im: Image.Image,
    width: int,
    height: int,
    position: ALIGNITEM,
) -> Image.Image:
    ratio = im.height / height
    im_width = width * ratio

    left, top = 0, 0
    if position == "start":
        left = 0

    elif position == "center":
        left = math.floor((im.width - im_width) / 2)
        im_width += left

    elif position == "end":
        left = math.floor(im.width - im_width)
        im_width = im.width

    return im.resize(
        size=(width, height),
        resample=Image.Resampling.LANCZOS,
        box=(left, top, im_width, im.height),
        reducing_gap=3,
    )
