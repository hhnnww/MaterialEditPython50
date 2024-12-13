import math
from functools import cached_property

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
)

from .class_layout_init import LayoutInit


class Layout1大N行自适应(LayoutInit):
    @cached_property
    def first_image(self) -> Image.Image:
        im = self._pil_list[0]

        first_height = math.ceil((self.xq_width) / (im.width / im.height))
        im = im.resize((self.xq_width, first_height), resample=Image.Resampling.LANCZOS)

        return im

    @cached_property
    def bottom_height(self) -> int:
        return self.xq_height - (self.spacing * 1) - self.first_image.height

    @cached_property
    def small_width(self) -> int:
        return math.ceil((self.xq_width - (self.spacing * 1)) / 2)

    def main(self):
        col_list = []
        bottom_list = []
        for pil in self._pil_list[1:]:
            small_height = math.ceil(self.small_width / (pil.width / pil.height))
            im = pil.resize(
                (self.small_width, small_height), resample=Image.Resampling.LANCZOS
            )

            col_list.append(im)

            col_height = sum([in_pil.height for in_pil in col_list]) + (
                (len(col_list) - 1) * self.spacing
            )

            if col_height >= self.bottom_height:
                col_im = fun_图片竖向拼接(
                    image_list=col_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.bg_color,
                )
                bottom_list.append(col_im.copy())
                col_list = []

            if len(bottom_list) == 2:
                break

        bottom_im = fun_图片横向拼接(
            image_list=bottom_list,
            spacing=self.spacing,
            align_item="start",
            background_color=self.bg_color,
        )

        bg = fun_图片竖向拼接(
            image_list=[self.first_image, bottom_im],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bg = bg.crop((0, 0, self.xq_width, self.xq_height))

        return bg
