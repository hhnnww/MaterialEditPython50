from PIL import Image, ImageDraw

from ..type import _COLOR


def fun_图片画边框(
    im: Image.Image, border_color: _COLOR, width: int = 1
) -> Image.Image:
    draw = ImageDraw.Draw(im)
    draw.line(((0, 0), (0, im.height - 1)), fill=border_color, width=width)
    draw.line(((0, 0), (im.width - 1, 0)), fill=border_color, width=width)
    draw.line(
        ((im.width - 1, 0), (im.width - 1, im.height - 1)),
        fill=border_color,
        width=width,
    )
    draw.line(
        ((0, im.height - 1), (im.width - 1, im.height - 1)),
        fill=border_color,
        width=width,
    )
    return im
