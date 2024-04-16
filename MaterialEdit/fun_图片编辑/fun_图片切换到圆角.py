from PIL import Image

from ..type import _COLOR
from .fun_画一个圆角矩形 import fun_画一个圆角矩形


def fun_图片切换到圆角(
    im: Image.Image, border_radius: int, background_color: _COLOR = (255, 255, 255, 0)
) -> Image.Image:
    circle_pil = fun_画一个圆角矩形(
        width=im.width,
        height=im.height,
        border_radius=border_radius,
    )

    bg = Image.new("RGBA", im.size, background_color)
    bg.paste(im, (0, 0), circle_pil)
    circle_pil.close()
    im.close()

    return bg
