import math

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO
from MaterialEdit.type import ImageModel


def layout_列自适应(
    image_list: list[ImageModel], col: int, xq_width: int, xq_height: int, spacing: int
):
    image_list = image_list + image_list + image_list
    col_width = math.ceil((xq_width - ((col + 1) * spacing)) / col)
    bg_height = xq_height - spacing

    in_line = []
    in_line_pil = []
    for image in image_list:
        # 处理小图
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        im = fun_图片裁剪(
            im=im,
            width=col_width,
            height=int(col_width / (im.width / im.height)),
            position="start",
        )

        # im.thumbnail((col_width, bg_height))

        if spacing > 0:
            im = fun_图片画边框(im, FIRST_IMAGE_BORDER_COLOR)
            im = fun_图片切换到圆角(im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

        in_line.append(im.copy())

        # 小图排成长图
        in_line_height = sum([im.height for im in in_line])
        if in_line_height > bg_height:
            inline_im = fun_图片竖向拼接(
                image_list=in_line,
                spacing=spacing,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )
            inline_im = inline_im.crop((0, 0, inline_im.width, bg_height))
            in_line_pil.append(inline_im.copy())
            in_line = []

        # 如果排列完成
        if len(in_line_pil) == col:
            break

    bg = fun_图片横向拼接(
        image_list=in_line_pil,
        spacing=spacing,
        align_item="start",
        background_color=(255, 255, 255, 255),
    )

    # bg = fun_图片裁剪(im=bg, width=xq_width, height=bg_height, position="start")

    bg = fun_图片扩大粘贴(
        im=bg,
        width=xq_width,
        height=xq_height,
        left="center",
        top="end",
        background_color=(255, 255, 255, 255),
    )

    return bg
