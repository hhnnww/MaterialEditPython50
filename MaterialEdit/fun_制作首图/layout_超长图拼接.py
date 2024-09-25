import math
from functools import cached_property
from itertools import cycle

from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片裁剪

from .class_layout_init import LayoutInit


class Layout超长图拼接(LayoutInit):
    @cached_property
    def fun_小图宽度(self) -> int:
        return math.ceil((self.xq_width - ((self.col - 1) * self.spacing)) / self.col)

    def main(self):
        line_list = []
        for im in cycle(self.pil_list):
            im = fun_图片裁剪(
                im=im,
                width=self.fun_小图宽度,
                height=self.xq_height,
                position=self.crop_position,
            )

            line_list.append(im)

            if len(line_list) == self.col:
                break

        bg = fun_图片横向拼接(
            image_list=line_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        bg = bg.crop((0, 0, self.xq_width, self.xq_height))

        return bg
