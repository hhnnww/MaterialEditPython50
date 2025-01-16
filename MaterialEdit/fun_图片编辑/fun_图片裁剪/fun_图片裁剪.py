from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_横图裁成竖图 import fun_横图裁成竖图
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_竖图裁成横图 import fun_竖图裁成横图
from MaterialEdit.type import ALIGNITEM


def fun_图片裁剪(
    im: Image.Image,
    width: int,
    height: int,
    position: ALIGNITEM,
) -> Image.Image:
    if im.width / im.height > width / height:
        return fun_横图裁成竖图(im=im, width=width, height=height, position=position)
    if im.width / im.height < width / height:
        return fun_竖图裁成横图(im=im, width=width, height=height, position=position)
    return im.resize(
        size=(width, height),
        resample=Image.Resampling.LANCZOS,
        box=(0, 0, im.width, im.height),
        reducing_gap=3,
    )
