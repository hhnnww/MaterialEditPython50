"""制作1+3的布局."""

from PIL import Image

from MaterialEdit.fun_图片编辑.class_image_edit import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
)
from MaterialEdit.type import ImageModel


def fun_layout_1_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
) -> Image.Image:
    """制作1+3的布局."""
    small_width = int((xq_width - ((3 - 1) * spacing)) / 3)
    small_height = int((xq_height - ((3 - 1) * spacing)) / 3)

    pil_list = []
    for num, image in enumerate(image_list):
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if num == 0:
            im = fun_图片裁剪(
                im,
                width=int(small_width * 3) + int(spacing * 2),
                height=int(small_height * 2) + int(spacing * 2),
                position="center",
            )
        else:
            # im = fun_图片裁剪(
            #     im,
            #     width=small_width,
            #     height=small_height,
            #     position="center",
            # )
            im = im.resize((small_width, small_height), Image.Resampling.LANCZOS)

        pil_list.append(im)
        max_len = 4
        if len(pil_list) == max_len:
            break

    top_pil = pil_list[0]
    two_pil = fun_图片横向拼接(pil_list[1:4], spacing, "center", (255, 255, 255, 255))
    bg = fun_图片竖向拼接([top_pil, two_pil], spacing, "start", (255, 255, 255, 255))
    return bg.resize((xq_width, xq_height), Image.Resampling.LANCZOS)
