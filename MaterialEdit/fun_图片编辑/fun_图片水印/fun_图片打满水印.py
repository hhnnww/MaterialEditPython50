from PIL import Image

from ...type import _COLOR
from ..fun_图片扩大粘贴 import fun_图片扩大粘贴
from ..fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from .fun_获取单个水印 import fun_获取单个水印


def fun_图片打满水印(
    im: Image.Image,
    size: int,
    line_number: int,
    singe_line_number: int,
    water_color: _COLOR,
):
    in_line_number = singe_line_number
    water_list = []
    for num in range(0, line_number):
        if num % 2 != 0:
            in_line_number += 1
        else:
            in_line_number = singe_line_number
        water_list.append(fun_单排水印(im.width, size, in_line_number, water_color))

    coly_spacing = int(
        ((im.height - 100) - sum([obj.height for obj in water_list]))
        / (len(water_list) - 1)
    )

    bg = fun_图片竖向拼接(water_list, coly_spacing, "center", (255, 255, 255, 0))
    bg = fun_图片扩大粘贴(bg, 9999, 9999, "center", "center", (255, 255, 255, 255), im)
    return bg


def fun_单排水印(
    im_width: int, size: int, single_line_number: int, water_color: _COLOR
):
    bg_width = int(im_width - 100)
    water_im = fun_获取单个水印(size=size, fill_clor=water_color)
    bg = Image.new("RGBA", (bg_width, water_im.height), (255, 255, 255, 0))

    top = 0
    if single_line_number == 1:
        spacing = int((bg_width - water_im.width) / 2)
        left = spacing
    else:
        if single_line_number % 2 == 0:
            spacing = int(
                (bg_width - (water_im.width * single_line_number))
                / (single_line_number - 1)
            )
            left = 0
        else:
            spacing = int(
                (bg_width - (water_im.width * single_line_number))
                / (single_line_number + 1)
            )
            left = spacing

    for x in range(0, single_line_number):
        bg.paste(water_im, (left, top), water_im)
        left += water_im.width + spacing

    return bg
