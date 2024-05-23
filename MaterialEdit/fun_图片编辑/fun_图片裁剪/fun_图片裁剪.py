from PIL import Image

from ...type import ALIGNITEM
from .fun_横图裁成竖图 import fun_横图裁成竖图
from .fun_竖图裁成横图 import fun_竖图裁成横图


def fun_图片裁剪(
    im: Image.Image, width: int, height: int, position: ALIGNITEM
) -> Image.Image:
    if im.width / im.height > width / height:
        return fun_横图裁成竖图(im=im, width=width, height=height, position=position)
    elif im.width / im.height < width / height:
        return fun_竖图裁成横图(im=im, width=width, height=height, position=position)
    else:
        return im.resize(
            size=(width, height),
            resample=Image.LANCZOS,
            box=(0, 0, im.width, im.height),
            reducing_gap=3,
        )
