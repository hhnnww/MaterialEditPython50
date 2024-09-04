from PIL import Image

from ..fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from ..fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from ..fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from ..fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from ..fun_图片编辑.fun_图片画边框 import fun_图片画边框
from ..fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from ..type import ImageModel


def fun_layout_1_2_3(
    image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int
):
    small_width = int((xq_width - ((3 + 1) * spacing)) / 3)
    small_height = int((xq_height - ((3 + 1) * spacing)) / 3)

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
                im, width=small_width, height=small_height, position="center"
            )

        if spacing > 0:
            im = fun_图片画边框(im, (240, 240, 240, 255))
            im = fun_图片切换到圆角(im, 15, (255, 255, 255, 255))

        pil_list.append(im)

        if len(pil_list) == 6:
            break

    large_right = fun_图片竖向拼接(
        [pil_list[1], pil_list[2]], spacing, "center", (255, 255, 255, 255)
    )
    top_pil = fun_图片横向拼接(
        [pil_list[0], large_right], spacing, "center", (255, 255, 255, 255)
    )

    two_pil = fun_图片横向拼接(pil_list[3:6], spacing, "center", (255, 255, 255, 255))

    bg = fun_图片竖向拼接([top_pil, two_pil], spacing, "start", (255, 255, 255, 255))
    bg = fun_图片扩大粘贴(
        bg, xq_width, xq_height, "center", "center", (255, 255, 255, 255)
    )

    return bg
