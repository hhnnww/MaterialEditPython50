from typing import Optional

from PIL import Image

from ..type import _COLOR, ALIGNITEM


def fun_图片扩大粘贴(
    im: Image.Image,
    width: int,
    height: int,
    left: ALIGNITEM,
    top: ALIGNITEM,
    background_color: _COLOR,
    background_pil: Optional[Image.Image] = None,
) -> Image.Image:
    if width < im.width:
        raise IndexError("背景宽度必须比图片尺寸大")

    if height < im.height:
        raise IndexError("背景高度必须比图片尺寸大")

    if background_pil is None:
        bg = Image.new("RGBA", (width, height), background_color)
    else:
        bg = background_pil
    l, t = 0, 0

    if left == "start":
        l = 0
    elif left == "center":
        l = int((bg.width - im.width) / 2)
    elif left == "end":
        l = bg.width - im.width

    if top == "start":
        t = 0
    elif top == "center":
        t = int((bg.height - im.height) / 2)
    elif top == "end":
        t = bg.height - im.height

    bg.paste(im, (l, t), im)

    im.close()

    return bg
