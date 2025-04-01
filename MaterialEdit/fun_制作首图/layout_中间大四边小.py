"""布局类 LayoutOneLargeOutSmall。"""

import math

from PIL import Image

from MaterialEdit.fun_制作首图.layout_1大3小_自适应 import LayoutInit
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class LayoutOneLargeOutSmall(LayoutInit):
    @property
    def small_size(self) -> tuple[int, int]:
        """计算小尺寸的宽度和高度。

        Returns:
            tuple[int, int]: 返回一个元组，包含计算得到的小尺寸宽度和高度。

        """
        width = math.ceil((self.xq_width - ((4 - 1) * self.spacing)) / 4)
        height = math.ceil(
            (self.xq_height - ((5 - 1) * self.spacing)) / 5,
        )
        return width, height

    @property
    def large_size(self) -> tuple[int, int]:
        """计算大尺寸的宽度和高度。

        根据小尺寸的宽度和高度，以及间距，计算出大尺寸的宽度和高度。
        返回:
            tuple[int, int]: 大尺寸的宽度和高度。
        """
        width = math.ceil((self.small_size[0] * 2) + self.spacing)
        height = math.ceil((self.small_size[1] * 2) + self.spacing)
        return width, height

    def main(self) -> Image.Image:
        """主函数用于生成一个拼接后的图片布局。

        功能描述：
        - 将多张图片按照指定的布局规则进行裁剪和拼接，生成最终的图片。
        - 布局分为三行：
            1. 第一行：横向拼接三张小图片。
            2. 第二行：左侧和右侧分别为一张小图片，中间为一张大图片，整体横向拼接。
            3. 第三行：横向拼接三张小图片。
        - 最终将三行图片竖向拼接为一个整体。
        参数：
        - 无直接参数，使用类的属性：
            - self._pil_list: 包含所有待处理图片的列表。
            - self.small_size: 小图片的宽高尺寸 (宽, 高)。
            - self.large_size: 大图片的宽高尺寸 (宽, 高)。
            - self.spacing: 图片之间的间距。
            - self.xq_width: 最终图片的宽度。
            - self.xq_height: 最终图片的高度。
        返回值：
        - 返回处理后的图片对象，尺寸为 (self.xq_width, self.xq_height)。
        """
        line_1 = fun_图片横向拼接(
            image_list=[
                fun_图片裁剪(
                    im=im,
                    width=self.small_size[0],
                    height=self.small_size[1],
                    position="center",
                )
                for im in self._pil_list[1:5]
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        line_2_left = fun_图片竖向拼接(
            image_list=[
                fun_图片裁剪(
                    im=im,
                    width=self.small_size[0],
                    height=self.small_size[1],
                    position="center",
                )
                for im in self._pil_list[5:7]
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        large_im = fun_图片裁剪(
            self._pil_list[0],
            width=self.large_size[0],
            height=self.large_size[1],
            position="center",
        )
        line_2_right = fun_图片竖向拼接(
            image_list=[
                fun_图片裁剪(
                    im=im,
                    width=self.small_size[0],
                    height=self.small_size[1],
                    position="center",
                )
                for im in self._pil_list[7:9]
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        line_2 = fun_图片横向拼接(
            image_list=[line_2_left, large_im, line_2_right],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        line_3 = fun_图片横向拼接(
            image_list=[
                fun_图片裁剪(
                    im=im,
                    width=self.small_size[0],
                    height=self.small_size[1],
                    position="center",
                )
                for im in self._pil_list[9:13]
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        line_4 = fun_图片横向拼接(
            image_list=[
                fun_图片裁剪(
                    im=im,
                    width=self.small_size[0],
                    height=self.small_size[1],
                    position="center",
                )
                for im in self._pil_list[13:17]
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )

        bg = fun_图片竖向拼接(
            image_list=[line_1, line_2, line_3, line_4],
            spacing=self.spacing,
            align_item="center",
            background_color=(0, 0, 0, 0),
        )
        return bg.resize((self.xq_width, self.xq_height), Image.Resampling.LANCZOS)
