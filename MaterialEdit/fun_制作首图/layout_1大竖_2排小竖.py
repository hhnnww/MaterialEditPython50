"""首图布局 1个大的竖图 旁边2排小的竖图."""

import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片竖向拼接, fun_图片裁剪


class Layout1大竖2排小竖(LayoutInit):
    @cached_property
    def fun_大图宽度(self) -> int:
        """去掉边距后的大图实际宽度"""
        im = self._pil_list[0]
        im_width = self.xq_height * (im.width / im.height)

        im_width = min(im_width, self.xq_width * 0.55)

        return math.ceil(im_width)

    @cached_property
    def fun_剩余宽度(self) -> int:
        """已经去掉了边距，只包含两行小图的实际宽度"""
        return self.xq_width - self.fun_大图宽度 - self.spacing

    @cached_property
    def fun_小图宽度(self) -> int:
        """去掉了中间边距的小图实际宽度"""
        return math.ceil((self.fun_剩余宽度 - self.spacing) / 2)

    @cached_property
    def fun_小图高度(self) -> int:
        """计算小图的高度."""
        return math.ceil((self.xq_height - (self.spacing * 2)) / 3)

    @property
    def fun_左边的大图(self) -> Image.Image:
        """构建左边的大图."""
        im = self._pil_list[0]
        return fun_图片裁剪(im, self.fun_大图宽度, self.xq_height, "center")

    def main(self) -> Image.Image:
        """开始制作图片."""
        line_list = []
        right_im_list = []

        for im in cycle(self._pil_list[1:]):
            in_im = fun_图片裁剪(
                im,
                width=self.fun_小图宽度,
                height=self.fun_小图高度,
                position="center",
            )

            line_list.append(in_im.copy())

            if self._fun_计算单行高度(im_list=line_list) > self.xq_height:
                line_im = fun_图片竖向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )

                right_im_list.append(line_im)

                line_list = []

            right_col = 2
            if len(right_im_list) == right_col:
                break

        right_im = fun_图片横向拼接(
            image_list=right_im_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片横向拼接(
            image_list=[self.fun_左边的大图, right_im],
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        return bg.crop((0, 0, self.xq_width, self.xq_height))
