"""超级长图拼接."""

import math
from functools import cached_property
from itertools import cycle

from PIL.Image import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片裁剪


class Layout超长图拼接(LayoutInit):
    @cached_property
    def fun_小图宽度(self) -> int:
        """计算小图宽度."""
        return math.ceil((self.xq_width - ((self.col - 1) * self.spacing)) / self.col)

    def main(self) -> Image:
        """开始制作长图."""
        line_list = []
        for im in cycle(self._pil_list):
            line_list.append(
                fun_图片裁剪(
                    im=im,
                    width=self.fun_小图宽度,
                    height=self.xq_height,
                    position=self.crop_position,
                ),
            )

            if len(line_list) == self.col:
                break

        bg = fun_图片横向拼接(
            image_list=line_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        return bg.crop((0, 0, self.xq_width, self.xq_height))
