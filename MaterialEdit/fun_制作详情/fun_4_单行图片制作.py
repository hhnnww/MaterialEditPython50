import math
from pathlib import Path

from PIL import Image, ImageFile

from MaterialEdit.fun_制作详情.fun_5_获取源文件 import fun_获取图片对应的源文件
from MaterialEdit.fun_制作详情.fun_6_小图增加信息 import fun_小图增加信息
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_图片打满水印 import fun_图片打满水印
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪

from ..type import ALIGNITEM, _ImageItem

ImageFile.LOAD_TRUNCATED_IMAGES = True


def fun_单行图片制作(
    image_list: list[_ImageItem],
    contains_info: bool,
    material_file_list: list[Path],
    xq_width: int,
    spacing: int,
    crop_position: ALIGNITEM,
    shop_name: str,
):
    image_used_width = math.ceil(xq_width - ((len(image_list) - 1) * spacing))
    # image_used_width = xq_width

    single_col_width = math.ceil(
        image_used_width / sum([image.ratio for image in image_list])
    )

    large_pic = False
    for image in image_list:
        if image.height is not None and image.width is not None:
            if image.height / image.width > 4:
                large_pic = True
                break

    left = []
    for image in image_list:
        if large_pic:
            image_width = image_used_width / len(image_list)
            image_height = image_width * 4
        else:
            image_width = single_col_width * image.ratio
            image_height = image_width / image.ratio

        im = Image.open(image.path)
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        im = fun_图片裁剪(
            im,
            width=math.ceil(image_width),
            height=math.ceil(image_height),
            position=crop_position,
        )

        # 画边框
        # pix_color = 240
        # im = fun_图片画边框(
        #     im=im, border_color=(pix_color, pix_color, pix_color, 255), width=1
        # )

        if shop_name != "泡泡素材":
            for water_piex_color in [0, 255]:
                im = fun_图片打满水印(
                    im=im,
                    size=120,
                    line_number=2,
                    singe_line_number=1,
                    water_color=(
                        water_piex_color,
                        water_piex_color,
                        water_piex_color,
                        math.ceil(255 * 0.5),
                    ),
                )
        else:
            water_piex_color = math.ceil(255 * 0.6)
            im = fun_图片打满水印(
                im=im,
                size=80,
                line_number=2,
                singe_line_number=1,
                water_color=(
                    water_piex_color,
                    water_piex_color,
                    water_piex_color,
                    math.ceil(255 * 0.8),
                ),
            )

        # 切换到圆角
        # im = fun_图片切换到圆角(
        #     im=im, border_radius=15, background_color=(255, 255, 255, 255)
        # )

        if contains_info is True:
            source_file = fun_获取图片对应的源文件(image.path, material_file_list)

            if source_file is None:
                title = Path(image.path).stem
                desc = "-"
            else:
                title = source_file.name
                if source_file.suffix.lower() in [".psd", ".psb"]:
                    desc = f"{image.width} × {image.height} (px)"
                elif source_file.suffix.lower() in [".ai", ".eps"]:
                    desc = "矢量设计素材"
                elif source_file.suffix.lower() in [".otf", ".ttf"]:
                    desc = f"{source_file.suffix.lower()} 字体文件素材"
                else:
                    desc = source_file.suffix.lower() + " 素材"

            im = fun_小图增加信息(im, title, desc)

        left.append(im)

    im = fun_图片横向拼接(
        left, spacing=spacing, align_item="start", background_color=(255, 255, 255, 255)
    )

    return im
