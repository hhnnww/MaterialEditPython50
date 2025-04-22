"""制作1大2中3小3小的布局."""

import math
from itertools import cycle

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.type import ImageModel


def fun_layout_1_2_3_3_3_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
    image_radio: int,
) -> Image.Image:
    """制作1大2中3小3小的布局."""
    small_width = math.floor((xq_width - ((3 + 1) * spacing)) / 3)
    small_height = math.floor((xq_height - ((5 + 1) * spacing)) / 6)

    pil_list = []
    for num, image in cycle(enumerate(image_list)):
        im = Image.open(image.path).convert("RGBA")

        if num == 0:
            im = ImageAction.fun_图片添加圆角(
                ImageAction.fun_图片裁剪(
                    im,
                    (int(small_width * 2) + spacing, int(small_height * 2) + spacing),
                    "start",
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

        max_num = 15
        if len(pil_list) == max_num:
            break

    large_right = ImageAction.fun_图片竖向拼接(
        [pil_list[1], pil_list[2]],
        spacing,
        "center",
    )
    top_pil = ImageAction.fun_图片横向拼接(
        [pil_list[0], large_right],
        spacing,
        "center",
    )

    two_pil = ImageAction.fun_图片横向拼接(pil_list[3:6], spacing, "center")
    three_pil = ImageAction.fun_图片横向拼接(pil_list[6:9], spacing, "center")
    four_pil = ImageAction.fun_图片横向拼接(pil_list[9:12], spacing, "center")
    five_pil = ImageAction.fun_图片横向拼接(
        pil_list[12:15],
        spacing,
        "center",
    )
    bg = ImageAction.fun_图片竖向拼接(
        [top_pil, two_pil, three_pil, four_pil, five_pil],
        spacing,
        "center",
    )

    return ImageAction.fun_图片扩大(
        bg,
        (xq_width, xq_height),
        Align.CENTER,
        Align.CENTER,
    )
