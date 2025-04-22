"""超级长图拼接."""

import math
from functools import cached_property
from itertools import cycle

from PIL.Image import Image

from image_action.image_action import ImageAction
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit


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
                ImageAction.fun_图片裁剪(
                    im=im,
                    size=(self.fun_小图宽度, self.xq_height),
                    align="start",
                ),
            )

            if len(line_list) == self.col:
                break

        bg = ImageAction.fun_图片横向拼接(
            image_list=line_list,
            spacing=self.spacing,
            align="start",
        )

        return bg.crop((0, 0, self.xq_width, self.xq_height))
