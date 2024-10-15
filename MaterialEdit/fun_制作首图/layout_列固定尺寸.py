import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
)

from .class_layout_init import LayoutInit


class Layout列固定尺寸(LayoutInit):
    @cached_property
    def fun_pil_list(self) -> list[Image.Image]:
        return [Image.open(image.path) for image in self.image_list]

    @cached_property
    def fun_平均比例(self) -> float:
        return sum([im.width / im.height for im in self.fun_pil_list]) / len(
            self.fun_pil_list
        )

    @cached_property
    def fun_small_width(self) -> int:
        return math.ceil((self.xq_width - (self.spacing * (self.col - 1))) / self.col)

    @cached_property
    def fun_small_height(self) -> int:
        return math.ceil(self.fun_small_width / self.fun_平均比例)

    def main(self):
        line_list = []
        all_list = []

        for im in cycle(self.image_list):
            print(im.path)
            im = Image.open(im.path)

            if im.mode.lower() != "rgba":
                im = im.convert("RGBA")

            im = fun_图片裁剪(
                im,
                width=self.fun_small_width,
                height=self.fun_small_height,
                position="center",
            )

            line_list.append(im.copy())

            if self._fun_计算单行高度(im_list=line_list) > self.xq_height:
                line_im = fun_图片竖向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.bg_color,
                )
                all_list.append(line_im.copy())

                line_list = []

            if len(all_list) == self.col:
                break

        bg = fun_图片横向拼接(
            image_list=all_list,
            spacing=self.spacing,
            align_item="start",
            background_color=self.bg_color,
        )

        bg = bg.crop((0, 0, self.xq_width, self.xq_height))

        # bg = fun_图片扩大粘贴(
        #     im=bg,
        #     width=self.xq_width,
        #     height=self.xq_height,
        #     left="center",
        #     top="end",
        #     background_color=(255, 255, 255, 255),
        # )

        return bg
