import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片扩大粘贴,
    fun_图片横向拼接,
    fun_图片竖向拼接,
)

from .class_layout_init import LayoutInit


class Layout小元素排列(LayoutInit):
    @cached_property
    def fun_小图高度(self) -> int:
        return math.ceil((self.xq_height - ((self.col - 1) * self.spacing)) / self.col)

    @cached_property
    def fun_小图宽度(self) -> int:
        return math.ceil(self.fun_小图高度 / self._fun_所有图片平均比例)

    def fun_计算行宽(self, im_list: list[Image.Image]) -> int:
        return sum([im.width for im in im_list]) + ((len(im_list) - 1) * self.spacing)

    def main(self):
        line_list = []
        bg_list = []

        for im in cycle(self._pil_list):
            im.thumbnail(
                (self.fun_小图宽度, self.fun_小图高度),
                resample=Image.Resampling.LANCZOS,
            )

            im = fun_图片扩大粘贴(
                im=im,
                width=self.fun_小图宽度,
                height=self.fun_小图高度,
                left="center",
                top="center",
                background_color=(255, 255, 255, 255),
            )

            line_list.append(im.copy())

            if self.fun_计算行宽(im_list=line_list) >= self.xq_width * 0.8:
                line_im = fun_图片横向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )
                bg_list.append(line_im.copy())
                line_list = []

            if len(bg_list) == self.col:
                break

        bg = fun_图片竖向拼接(
            image_list=bg_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        bg.thumbnail((self.xq_width, self.xq_height), resample=Image.Resampling.LANCZOS)

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )

        return bg
