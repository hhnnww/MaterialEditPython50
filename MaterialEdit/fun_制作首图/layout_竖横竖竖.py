from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO
from MaterialEdit.type import ImageModel


def layout_竖横竖竖(
    image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int
):
    im1_width = int(((xq_width - (spacing * 3)) / 5) * 2)
    im1_height = int(xq_height - (spacing * 2))
    im1 = Image.open(image_list[0].path)
    im1 = im1.convert("RGBA")
    im1 = fun_图片裁剪(im=im1, width=im1_width, height=im1_height, position="center")
    if spacing > 0:
        im1 = fun_图片画边框(im1, FIRST_IMAGE_BORDER_COLOR)
        im1 = fun_图片切换到圆角(im1, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    im2_width = int(((xq_width - (spacing * 3)) / 5) * 3)
    im2_height = int(((xq_height - (spacing * 3)) / 5) * 2)
    im2 = Image.open(image_list[1].path)
    im2 = im2.convert("RGBA")
    im2 = fun_图片裁剪(im=im2, width=im2_width, height=im2_height, position="center")
    if spacing > 0:
        im2 = fun_图片画边框(im2, FIRST_IMAGE_BORDER_COLOR)
        im2 = fun_图片切换到圆角(im2, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    im34_width = int((im2_width - spacing) / 2)
    im34_height = int(((xq_height - (spacing * 3)) / 5) * 3)

    im3 = Image.open(image_list[2].path)
    im3 = im3.convert("RGBA")
    im3 = fun_图片裁剪(im=im3, width=im34_width, height=im34_height, position="center")
    if spacing > 0:
        im3 = fun_图片画边框(im3, FIRST_IMAGE_BORDER_COLOR)
        im3 = fun_图片切换到圆角(im3, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    im4 = Image.open(image_list[3].path)
    im4 = im4.convert("RGBA")
    im4 = fun_图片裁剪(im=im4, width=im34_width, height=im34_height, position="center")
    if spacing > 0:
        im4 = fun_图片画边框(im4, FIRST_IMAGE_BORDER_COLOR)
        im4 = fun_图片切换到圆角(im4, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    im34_bg = fun_图片横向拼接(
        image_list=[im3, im4],
        spacing=spacing,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )
    right_bg = fun_图片竖向拼接(
        image_list=[im2, im34_bg],
        spacing=spacing,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )
    bg = fun_图片横向拼接(
        image_list=[im1, right_bg],
        spacing=spacing,
        align_item="center",
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
