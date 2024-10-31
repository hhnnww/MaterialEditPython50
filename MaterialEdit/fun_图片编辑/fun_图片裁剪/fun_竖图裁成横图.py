import math

from PIL import Image

from ...type import ALIGNITEM


def fun_竖图裁成横图(
    im: Image.Image, width: int, height: int, position: ALIGNITEM
) -> Image.Image:
    ratio = im.width / width
    im_height = height * ratio

    top, _bottom = 0, 0
    if position == "start":
        top = 0

    elif position == "center":
        top = math.floor((im.height - im_height) / 2)
        im_height += top

    elif position == "end":
        top = math.floor(im.height - im_height)
        im_height = im.height

    return im.resize(
        size=(width, height),
        resample=Image.Resampling.LANCZOS,
        box=(0, top, im.width, im_height),
        reducing_gap=3,
    )
