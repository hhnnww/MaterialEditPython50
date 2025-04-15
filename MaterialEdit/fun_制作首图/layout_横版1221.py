"""横版1221布局"""

import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from image_action import ImageAction
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class LayoutHorizontal1221(LayoutInit):
    """LayoutHorizontal1221类。

    此类继承自 LayoutInit 用于生成横版1221布局的图片。
    属性:
        fun_小图尺寸 (tuple[int, int]): 计算小图的宽度和高度。
        fun_大图尺寸 (tuple[int, int]): 计算大图的宽度和高度。
    方法:
        fun_横版1221() -> Image.Image:
            生成横版1221布局的图片。
    参数:
        Image.Image: 生成的横版1221布局图片。
    """

    @cached_property
    def fun_小图尺寸(self) -> tuple[int, int]:
        """计算小图的尺寸。

        计算出小图的宽度和高度，并返回一个包含宽度和高度的元组。
        返回:
            tuple[int, int]: 小图的宽度和高度。
        """
        small_width = math.ceil((self.xq_width - (self.spacing * 2)) / 3) + 50
        small_height = math.ceil((self.xq_height - (self.spacing * 3)) / 4)
        return (small_width, small_height)

    @cached_property
    def fun_大图尺寸(self) -> tuple[int, int]:
        """计算大图的尺寸。

        根据小图的尺寸和间距，计算出大图的宽度和高度。
        返回:
            tuple[int, int]: 大图的宽度和高度。
        """
        width = (self.fun_小图尺寸[0] * 2) + self.spacing - 50
        height = (self.fun_小图尺寸[1] * 2) + self.spacing
        return (width, height)

    def fun_横版1221(self) -> Image.Image:
        """生成横版1221布局的图片。

        此方法从 `self.image_list` 中循环获取图片，裁剪并拼接成指定的布局格式。
        最终生成的图片会被调整为指定的输出尺寸。
        步骤：
        1. 从 `self.image_list` 中依次获取图片，裁剪为大图或小图尺寸。
           - 第 1 张和第 6 张图片裁剪为大图尺寸（`self.fun_大图尺寸`）。
           - 其余图片裁剪为小图尺寸（`self.fun_小图尺寸`）。
        2. 将裁剪后的图片按照以下布局拼接：
           - 上半部分：第 1 张图片与第 2、3 张图片竖向拼接后的结果横向拼接。
           - 下半部分：第 4、5 张图片竖向拼接后的结果与第 6 张图片横向拼接。
           - 最终：将上半部分与下半部分竖向拼接。
        3. 调整拼接后的图片为指定的输出尺寸（`self.xq_width` 和 `self.xq_height`）。
        参数：
            无参数，使用类的属性：
            - `self.image_list`：图片路径列表。
            - `self.fun_大图尺寸`：大图裁剪尺寸 (宽, 高)。
            - `self.fun_小图尺寸`：小图裁剪尺寸 (宽, 高)。
            - `self.crop_position`：裁剪位置。
            - `self.spacing`：图片拼接时的间距。
            - `self.bg_color`：拼接时的背景颜色。
            - `self.xq_width`：输出图片的宽度。
            - `self.xq_height`：输出图片的高度。
        """
        image_list = cycle(self.image_list)
        max_num = 6
        num = 1
        im_list = []
        for image in image_list:
            im = Image.open(image.path)
            im = im.convert("RGBA")
            if num in [1, 6]:
                im_list.append(
                    fun_图片裁剪(
                        im,
                        width=self.fun_大图尺寸[0],
                        height=self.fun_大图尺寸[1],
                        position=self.crop_position,
                    ),
                )
            else:
                im_list.append(
                    fun_图片裁剪(
                        im,
                        width=self.fun_小图尺寸[0],
                        height=self.fun_小图尺寸[1],
                        position=self.crop_position,
                    ),
                )

            num += 1

            if len(im_list) == max_num:
                break

        top_r = ImageAction.ImageMerge(
            image_list=[im_list[1], im_list[2]],
            spacing=self.spacing,
            align="center",
            direction="x",
        ).main()

        top = fun_图片横向拼接(
            image_list=[im_list[0], top_r],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bottom_l = fun_图片竖向拼接(
            image_list=[im_list[3], im_list[4]],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bottom = fun_图片横向拼接(
            image_list=[bottom_l, im_list[5]],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bg = fun_图片竖向拼接(
            image_list=[top, bottom],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        return bg.resize((self.xq_width, self.xq_height), Image.Resampling.LANCZOS)
