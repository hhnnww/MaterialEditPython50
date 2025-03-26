"""图片扩大粘贴"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from MaterialEdit.type import _COLOR, ALIGNITEM


def fun_图片扩大粘贴(
    im: Image.Image,
    width: int,
    height: int,
    left: ALIGNITEM,
    top: ALIGNITEM,
    background_color: _COLOR,
    background_pil: Image.Image | None = None,
) -> Image.Image:
    """吧图片扩大，并可以添加背景颜色."""
    if width < im.width:
        msg = "背景宽度必须比图片尺寸大"
        raise IndexError(msg)

    if height < im.height:
        msg = "背景高度必须比图片尺寸大"
        raise IndexError(msg)

    if background_pil is None:
        bg = Image.new("RGBA", (width, height), background_color)
    else:
        bg = background_pil
    left_position, t = 0, 0

    if left == "start":
        left_position = 0
    elif left == "center":
        left_position = int((bg.width - im.width) / 2)
    elif left == "end":
        left_position = bg.width - im.width

    if top == "start":
        t = 0
    elif top == "center":
        t = int((bg.height - im.height) / 2)
    elif top == "end":
        t = bg.height - im.height

    bg.paste(im, (left_position, t), im)

    im.close()

    return bg
