from PIL import Image, ImageDraw

from .fun_画一个圆形 import fun_画一个圆
from ..type import _COLOR


def fun_画一个圆形横框(
    width: int, height: int, fill_color: _COLOR = (255, 255, 255, 255), background_color: _COLOR = (255, 255, 255, 0)
):
    bg = Image.new("RGBA", (width, height), background_color)
    circle = fun_画一个圆(width=height, height=height, fill_color=fill_color, background_color=background_color)
    bg.paste(circle, (0, 0), circle)
    bg.paste(circle, (bg.width - circle.width, 0), circle)
    draw = ImageDraw.Draw(bg)
    draw.rectangle((int(height / 2), 0, int(width - (height / 2)), height), fill=fill_color)

    return bg
