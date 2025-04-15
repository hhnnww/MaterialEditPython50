"""Module provides functions to create a layout

with 1 large, 2 medium,and 3 small images.
"""

from itertools import cycle

from PIL import Image

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
) -> Image.Image:
    """制作1大2中3小的布局."""
    small_width = int((xq_width - ((3 - 1) * spacing)) / 3)
    small_height = int((xq_height - ((4 - 1) * spacing)) / 4)

    pil_list = []
    for num, image in enumerate(cycle(image_list)):
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if num == 0:
            im = im.resize(
                (int(small_width * 2) + spacing, int(small_height * 2) + spacing),
                resample=Image.Resampling.LANCZOS,
            )
        else:
            im = im.resize(
                (small_width, small_height),
                resample=Image.Resampling.LANCZOS,
            )

        pil_list.append(im)
        max_len = 9
        if len(pil_list) == max_len:
            break

    large_right = fun_图片竖向拼接(
        [pil_list[1], pil_list[2]],
        spacing,
        "center",
        (255, 255, 255, 255),
    )
    top_pil = fun_图片横向拼接(
        [pil_list[0], large_right],
        spacing,
        "center",
        (255, 255, 255, 255),
    )

    two_pil = fun_图片横向拼接(
        pil_list[3:6],
        spacing,
        "center",
        (255, 255, 255, 255),
    )
    three_pil = fun_图片横向拼接(
        pil_list[6:9],
        spacing,
        "center",
        (255, 255, 255, 255),
    )

    bg = fun_图片竖向拼接(
        [top_pil, two_pil, three_pil],
        spacing,
        "start",
        (255, 255, 255, 255),
    )
    return bg.resize((xq_width, xq_height), Image.Resampling.LANCZOS)
