"""Module provides functions to create a layout

with 1 large, 2 medium,and 3 small images.
"""

from itertools import cycle

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_图片编辑 import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
)
from MaterialEdit.type import ImageModel


def fun_layout_1_2_3_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
    radio: bool,
    bg_color: tuple[int, int, int, int] | tuple[int, int, int],
) -> Image.Image:
    """制作1大2中3小的布局."""
    image_radio = 0
    if radio is True:
        image_radio = 20

    if radio is False:
        small_width = int((xq_width - ((3 - 1) * spacing)) / 3)
        small_height = int((xq_height - ((4 - 1) * spacing)) / 4)
    else:
        small_width = int((xq_width - ((3 + 1) * spacing)) / 3)
        small_height = int((xq_height - ((4 + 1) * spacing)) / 4)

    pil_list = []
    for num, image in enumerate(cycle(image_list)):
        im = Image.open(image.path).convert("RGBA")

        if num == 0:
            im = ImageAction.fun_图片添加圆角(
                ImageAction.fun_图片裁剪(
                    im,
                    (int(small_width * 2) + spacing, int(small_height * 2) + spacing),
                    "center",
                ),
                image_radio,
            )
        else:
            im = ImageAction.fun_图片添加圆角(
                ImageAction.fun_图片裁剪(
                    im,
                    (small_width, small_height),
                    "center",
                ),
                image_radio,
            )

        pil_list.append(im)
        max_len = 9
        if len(pil_list) == max_len:
            break

    large_right = fun_图片竖向拼接(
        [pil_list[1], pil_list[2]],
        spacing,
        "center",
        bg_color,
    )
    top_pil = fun_图片横向拼接(
        [pil_list[0], large_right],
        spacing,
        "center",
        bg_color,
    )

    two_pil = fun_图片横向拼接(
        pil_list[3:6],
        spacing,
        "center",
        bg_color,
    )
    three_pil = fun_图片横向拼接(
        pil_list[6:9],
        spacing,
        "center",
        bg_color,
    )

    bg = fun_图片竖向拼接(
        [top_pil, two_pil, three_pil],
        spacing,
        "start",
        bg_color,
    )

    return ImageAction.fun_图片添加背景(
        ImageAction.fun_图片扩大(
            bg,
            (xq_width, xq_height),
            Align.CENTER,
            Align.CENTER,
        ),
        bg_color,
    )
