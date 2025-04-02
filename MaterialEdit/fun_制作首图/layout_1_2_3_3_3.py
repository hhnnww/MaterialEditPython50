"""制作1大2中3小3小的布局."""

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.type import ImageModel


def fun_layout_1_2_3_3_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
    bg_color: tuple,
) -> Image.Image:
    """制作1大2中3小3小的布局."""
    small_width = int((xq_width - ((3 - 1) * spacing)) / 3)
    small_height = int((xq_height - ((5 - 1) * spacing)) / 5)

    pil_list = []
    for num, image in enumerate(image_list):
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if num == 0:
            im = fun_图片裁剪(
                im,
                width=int(small_width * 2) + spacing,
                height=int(small_height * 2) + spacing,
                position="center",
            )
        else:
            im = fun_图片裁剪(
                im,
                width=small_width,
                height=small_height,
                position="center",
            )

        pil_list.append(im)

        max_num = 12
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

    two_pil = fun_图片横向拼接(pil_list[3:6], spacing, "center", bg_color)
    three_pil = fun_图片横向拼接(pil_list[6:9], spacing, "center", bg_color)
    four_pil = fun_图片横向拼接(pil_list[9:12], spacing, "center", bg_color)

    bg = fun_图片竖向拼接(
        [top_pil, two_pil, three_pil, four_pil],
        spacing,
        "start",
        bg_color,
    )
    return fun_图片扩大粘贴(
        bg,
        xq_width,
        xq_height,
        "center",
        "center",
        bg_color,
    )
