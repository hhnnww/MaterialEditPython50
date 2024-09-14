from PIL import Image

from MaterialEdit.setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO

from ..fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from ..fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from ..fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from ..fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from ..fun_图片编辑.fun_图片画边框 import fun_图片画边框
from ..fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from ..type import ImageModel


def layout_3列1大横竖错落(
    image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int
):
    small_width = int((xq_width - (spacing * 4)) / 3)
    small_height = int((xq_height - (spacing * 5)) / 4)

    large_im = Image.open(image_list[0].path)
    large_im = large_im.convert("RGBA")
    large_im = fun_图片裁剪(
        large_im,
        width=int((small_width * 2) + spacing),
        height=int((small_height * 2) + spacing),
        position="center",
    )
    if spacing > 0:
        large_im = fun_图片画边框(large_im, FIRST_IMAGE_BORDER_COLOR)
        large_im = fun_图片切换到圆角(large_im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    small_im_list = []
    for image in image_list[1:]:
        print(f"制作首图：{image.path}")
        im = Image.open(image.path)
        if im.mode != "rgba":
            im = im.convert("RGBA")

        if im.width >= im.height:
            im = fun_图片裁剪(
                im=im, width=small_width, height=small_height, position="center"
            )
        else:
            im = fun_图片裁剪(
                im=im,
                width=small_width,
                height=int((small_height * 2) + spacing),
                position="center",
            )

        if spacing > 0:
            im = fun_图片画边框(im, FIRST_IMAGE_BORDER_COLOR)
            im = fun_图片切换到圆角(im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

        small_im_list.append(im.copy())

    bottom_line_list = []
    bottom_list = []

    num = 0
    for bottom_small_im in small_im_list:
        bottom_line_list.append(bottom_small_im.copy())
        num += 1
        bottom_line_height = sum([im_h.height for im_h in bottom_line_list])
        if bottom_line_height > int((small_height * 2) * 0.8):
            if len(bottom_line_list) == 1:
                bottom_list.append(bottom_line_list[0].copy())
                bottom_line_list = []

            elif len(bottom_line_list) > 1:
                bottom_col_line_im = fun_图片竖向拼接(
                    image_list=bottom_line_list,
                    spacing=spacing,
                    align_item="start",
                    background_color=(255, 255, 255, 255),
                )
                bottom_list.append(bottom_col_line_im.copy())
                bottom_line_list = []

        if len(bottom_list) == 2:
            bottom_im = fun_图片横向拼接(
                image_list=bottom_list,
                spacing=spacing,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )
            left_im = fun_图片竖向拼接(
                image_list=[large_im, bottom_im],
                spacing=spacing,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )
            break

    right_list = []
    for im in small_im_list[num:]:
        print(num)
        right_list.append(im.copy())
        right_im_height = sum([im.height for im in right_list])
        if right_im_height > int((small_height * 4) * 0.8):
            right_im = fun_图片竖向拼接(
                image_list=right_list,
                spacing=spacing,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )
            break

    bg = fun_图片横向拼接(
        image_list=[left_im, right_im],
        spacing=spacing,
        align_item="start",
        background_color=(255, 255, 255, 255),
    )
    bg = fun_图片扩大粘贴(
        im=bg,
        width=xq_width,
        height=xq_height,
        left="center",
        top="center",
        background_color=(255, 255, 255, 255),
    )

    return bg
