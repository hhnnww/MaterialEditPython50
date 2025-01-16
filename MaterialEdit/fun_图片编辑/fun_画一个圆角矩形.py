from PIL import Image, ImageDraw

from MaterialEdit.type import _COLOR


def fun_画一个圆角矩形(
    width: int,
    height: int,
    border_radius: int,
    fill_color: _COLOR = (255, 255, 255, 255),
    background_color: _COLOR = (255, 255, 255, 0),
    large_ratio: int = 3,
):
    large_width = width * large_ratio
    large_height = height * large_ratio
    im = Image.new("RGBA", (large_width, large_height), background_color)

    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        xy=(0, 0, im.width, im.height),
        radius=border_radius * large_ratio,
        fill=fill_color,
    )

    im.thumbnail((width, height), resample=Image.Resampling.LANCZOS, reducing_gap=3)
    return im
