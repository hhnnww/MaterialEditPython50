from PIL import Image, ImageDraw

from ..type import _COLOR


def fun_画一个圆(
    width: int,
    height: int,
    fill_color: _COLOR = (255, 255, 255, 255),
    background_color: _COLOR = (255, 255, 255, 0),
    ratio: int = 3,
) -> Image.Image:
    large_width = width * ratio
    large_height = height * ratio
    im = Image.new("RGBA", (large_width, large_height), background_color)
    draw = ImageDraw.Draw(im)
    draw.ellipse(xy=(0, 0, large_width, large_height), fill=fill_color)
    im.thumbnail((width, height), resample=Image.LANCZOS, reducing_gap=3)
    return im
