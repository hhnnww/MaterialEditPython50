"""制作1大2中3小3小的布局."""

from itertools import cycle

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.type import ImageModel


def fun_layout_1_2_3_3_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
    bg_color: tuple,
    radio: bool,
) -> Image.Image:
    image_radio = 0
    if radio is True:
        image_radio = 20

    """制作1大2中3小3小的布局."""
    if radio is False:
        small_width = int((xq_width - ((3 - 1) * spacing)) / 3)
        small_height = int((xq_height - ((5 - 1) * spacing)) / 5)
    else:
        small_width = int((xq_width - ((3 + 1) * spacing)) / 3)
        small_height = int((xq_height - ((5 + 1) * spacing)) / 5)

    pil_list = []
    max_num = 12
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

        if len(pil_list) == max_num:
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

    bg = ImageAction.fun_图片竖向拼接(
        image_list=[
            top_pil,
            ImageAction.fun_图片横向拼接(
                image_list=pil_list[3:6],
                spacing=spacing,
                align="center",
            ),
            ImageAction.fun_图片横向拼接(
                image_list=pil_list[6:9],
                spacing=spacing,
                align="center",
            ),
            ImageAction.fun_图片横向拼接(
                image_list=pil_list[9:12],
                spacing=spacing,
                align="center",
            ),
        ],
        spacing=spacing,
        align="start",
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
