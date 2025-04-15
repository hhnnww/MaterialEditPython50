"""fun_layout_1_2_3 函数用于根据给定的图片列表和尺寸参数生成特定布局的图片。

参数:
    image_list (list[ImageModel]): 包含图片路径和元数据的 ImageModel 对象列表。
    xq_width (int): 输出图片的目标宽度。
    xq_height (int): 输出图片的目标高度。
    spacing (int): 图片之间的间距。
返回:
    PIL.Image.Image: 按照指定布局生成的图片。
功能:
    - 将图片裁剪为指定大小。
    - 按照 1-2-3 的布局规则拼接图片：
        - 第一张图片占据左上角较大的区域。
        - 第二、三张图片垂直拼接在右上角。
        - 第四、五、六张图片水平拼接在下方。
    - 最终生成的图片调整为目标尺寸。
"""

from itertools import cycle
from math import ceil

from PIL import Image

import image_action
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.type import ImageModel


def fun_layout_1_2_3(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
) -> Image.Image:
    """根据提供的图片列表生成一个特定布局的拼接图片。

    此函数将图片按照 1-2-3 的布局规则进行裁剪和拼接，最终生成一个指定大小的图片。
    布局规则如下：
    - 第一张图片占据左上角的大区域。
    - 第二张和第三张图片垂直拼接，占据右上角的区域。
    - 第四张、第五张和第六张图片水平拼接，占据下方的区域。
    参数:
        image_list (list[ImageModel]): 包含图片路径的 ImageModel 对象列表。
        xq_width (int): 最终生成图片的宽度。
        xq_height (int): 最终生成图片的高度。
        spacing (int): 图片之间的间距。
    返回:
        Image.Image: 生成的拼接图片，大小为 (xq_width, xq_height)。
    """
    small_width = ceil((xq_width - ((3 + 1) * spacing)) / 3)
    small_height = ceil((xq_height - ((3 + 1) * spacing)) / 3)

    pil_list = []
    for num, image in enumerate(cycle(image_list)):
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if num == 0:
            im = image_action.ImageAction.ImageCrop.fun_图片裁剪(
                im=im,
                size=((small_width * 2) + spacing, (small_height * 2) + spacing),
                align="center",
            )
        else:
            im = image_action.ImageAction.ImageCrop.fun_图片裁剪(
                im=im,
                size=(small_width, small_height),
                align="center",
            )

        pil_list.append(im.copy())
        max_num = 6
        if len(pil_list) == max_num:
            break

    large_right = fun_图片竖向拼接(
        [pil_list[1], pil_list[2]],
        spacing,
        "center",
        (255, 255, 255, 255),
    )
    top_pil = fun_图片横向拼接(
        [pil_list[0], large_right],
        spacing,
        "center",
        (255, 255, 255, 255),
    )

    two_pil = fun_图片横向拼接(pil_list[3:6], spacing, "center", (255, 255, 255, 255))

    bg = fun_图片竖向拼接([top_pil, two_pil], spacing, "start", (255, 255, 255, 255))

    return bg.resize((xq_width, xq_height), Image.Resampling.LANCZOS)
