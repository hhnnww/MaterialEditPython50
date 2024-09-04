from PIL import Image

from ..fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from ..fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from ..fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from ..fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from ..type import ImageModel


def layout_3列横竖错落(
    image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int
):
    col_width = int((xq_width - (spacing * 4)) / 3)
    col_height = int((xq_height - (spacing * 5)) / 4)

    # 大图列表
    bg_im_list = []

    # col_im 每个列的列表
    col_line_im_list = []
    for image in image_list:
        print(f"处理首图小图{image.path}")
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if im.width >= im.height:
            im = fun_图片裁剪(
                im=im, width=col_width, height=col_height, position="center"
            )
        else:
            im = fun_图片裁剪(
                im=im,
                width=col_width,
                height=int((col_height * 2) + spacing),
                position="center",
            )

        col_line_im_list.append(im.copy())

        # 计算每一列的高度，如果高度大于详情图的90%
        # 拼接小图,并且传入到背景图列表
        col_line_height = sum([im.height for im in col_line_im_list]) + int(
            len(col_line_im_list) * spacing
        )

        if col_line_height > xq_height * 0.9:
            line_im = fun_图片竖向拼接(
                image_list=col_line_im_list,
                spacing=spacing,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )
            bg_im_list.append(line_im)
            col_line_im_list = []

        if len(bg_im_list) == 3:
            break

    bg = fun_图片横向拼接(
        bg_im_list,
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
