"""制作1+n的布局."""

import math

from PIL import Image

from MaterialEdit.fun_图片编辑.class_image_edit import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
)
from MaterialEdit.type import ImageModel


def fun_layout_1_n(
    image_list: list[ImageModel],
    small_line_num: int,
    xq_width: int,
    xq_height: int,
    spacing: int,
) -> Image.Image:
    """制作1+n的布局."""
    # 组合图片编组
    comb_image_list = [[image_list[0]], image_list[1 : small_line_num + 1]]

    # 计算大图的高度
    larger_image_width = xq_width
    larger_image_height = float(larger_image_width) / image_list[0].ratio

    # 计算小图的高度
    small_image_all_width = math.ceil(xq_width - spacing)

    small_image_all_height = small_image_all_width / sum(
        [obj.ratio for obj in comb_image_list[1]],
    )

    # 计算图片合并起来之后需要缩小的比例
    all_reduce_ratio = (xq_height - spacing) / (
        larger_image_height + small_image_all_height
    )

    # 制作大图
    large_im = Image.open(comb_image_list[0][0].path)
    if large_im.mode != "RGBA":
        large_im = large_im.convert("RGBA")

    large_im = fun_图片裁剪(
        large_im,
        larger_image_width,
        math.ceil(larger_image_height * all_reduce_ratio),
        "center",
    )

    # 制作小图
    all_small_pil = []
    for image in comb_image_list[1]:
        small_im_width = math.ceil(
            (small_image_all_width / sum([obj.ratio for obj in comb_image_list[1]]))
            * image.ratio,
        )
        small_im_height = math.ceil(small_im_width / image.ratio * all_reduce_ratio)
        small_im = Image.open(image.path)
        if small_im != "RGBA":
            small_im = small_im.convert("RGBA")
        small_im = fun_图片裁剪(
            small_im,
            small_im_width,
            small_im_height,
            "center",
        )

        all_small_pil.append(small_im.copy())

    small_line_im = fun_图片横向拼接(
        all_small_pil,
        spacing=spacing,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    small_line_im = small_line_im.resize(
        (large_im.width, small_line_im.height),
        resample=Image.Resampling.LANCZOS,
    )

    bg = fun_图片竖向拼接(
        [large_im, small_line_im],
        spacing,
        "center",
        (255, 255, 255, 255),
    )
    return bg.resize((xq_width, xq_height), Image.Resampling.LANCZOS)
