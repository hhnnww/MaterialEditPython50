import math
from itertools import cycle
from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.type import ALIGNITEM, ImageModel


def layout_列自适应(
    image_list: list[ImageModel],
    col: int,
    xq_width: int,
    xq_height: int,
    spacing: int,
    crop_position: ALIGNITEM,
    design_path: str,
) -> Image.Image:
    """列自适应首图."""
    bg_color = (255, 255, 255, 0)
    col_width = math.ceil((xq_width - ((col - 1) * spacing)) / col)

    in_line = []
    in_line_pil = []

    for image in cycle(image_list):
        # 处理小图
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert(mode="RGBA")

        im = fun_图片裁剪(
            im=im,
            width=col_width,
            height=math.ceil(col_width / (im.width / im.height)),
            position=crop_position,
        )

        in_line.append(im.copy())

        # 小图排成长图
        in_line_height = sum([im.height for im in in_line])
        if in_line_height > xq_height:
            inline_im = fun_图片竖向拼接(
                image_list=in_line,
                spacing=spacing,
                align_item="start",
                background_color=bg_color,
            )

            in_line_pil.append(inline_im.copy())
            in_line = []

        # 如果排列完成
        if len(in_line_pil) == col:
            break

    bg = fun_图片横向拼接(
        image_list=in_line_pil,
        spacing=spacing,
        align_item="start",
        background_color=bg_color,
    )

    if Path(design_path).exists() is not True:
        Path(design_path).mkdir()

    design_img = f"{len(list(Path(design_path).iterdir()))}.png"
    bg.save((Path(design_path) / f"{design_img}").as_posix())

    return fun_图片裁剪(im=bg, width=xq_width, height=xq_height, position="start")
