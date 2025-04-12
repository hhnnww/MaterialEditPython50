"""3*3布局

左上角放一个小图2*2的大图
右上角放一个小图2*1的图
底部放3个小图1*1的图
"""

import math

from PIL import Image

from MaterialEdit.fun_制作首图.layout_1大3小_自适应 import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接


class Layout1Large3Small(LayoutInit):
    @property
    def small_width(self) -> int:
        """小图宽度."""
        return math.ceil((self.xq_width - (2 * self.spacing)) / 3)

    @property
    def small_height(self) -> int:
        """小图高度."""
        return math.ceil((self.xq_height - (2 * self.spacing)) / 3)

    @property
    def first_size(self) -> tuple[int, int]:
        """大图尺寸."""
        return math.ceil((self.small_width * 2) + self.spacing), math.ceil(
            (self.small_height * 2) + self.spacing,
        )

    def first_image(self) -> Image.Image:
        """获取大图."""
        return self._pil_list[0].resize(
            self.first_size,
            Image.Resampling.LANCZOS,
        )

    def right_image(self) -> Image.Image:
        """获取右上小图."""
        return fun_图片竖向拼接(
            image_list=[
                self._pil_list[1].resize(
                    (self.small_width, self.small_height),
                    resample=Image.Resampling.LANCZOS,
                ),
                self._pil_list[2].resize(
                    (self.small_width, self.small_height),
                    resample=Image.Resampling.LANCZOS,
                ),
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

    def bottom_one(self) -> Image.Image:
        """获取下方小图."""
        return fun_图片横向拼接(
            image_list=[
                self._pil_list[3].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
                self._pil_list[4].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
                self._pil_list[5].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

    def bottom_two(self) -> Image.Image:
        """获取下方小图."""
        return fun_图片横向拼接(
            image_list=[
                self._pil_list[6].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
                self._pil_list[7].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
                self._pil_list[8].resize(
                    (self.small_width, self.small_height),
                    Image.Resampling.LANCZOS,
                ),
            ],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

    def main(self) -> Image.Image:
        """主函数."""
        top_one = fun_图片横向拼接(
            image_list=[self.first_image(), self.right_image()],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )
        bg = fun_图片竖向拼接(
            image_list=[top_one, self.bottom_one()],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )
        return bg.resize(
            (self.xq_width, self.xq_height),
            Image.Resampling.LANCZOS,
        )
