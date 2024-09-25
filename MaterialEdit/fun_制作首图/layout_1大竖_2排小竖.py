import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片竖向拼接, fun_图片裁剪

from .class_layout_init import LayoutInit


class Layout1大竖2排小竖(LayoutInit):
    @cached_property
    def fun_大图宽度(self) -> int:
        """去掉边距后的大图实际宽度"""
        im = self.pil_list[0]
        im_width = self.xq_height * (im.width / im.height)

        if im_width > self.xq_width * 0.55:
            im_width = self.xq_width * 0.55

        return math.ceil(im_width)

    @cached_property
    def fun_剩余宽度(self) -> int:
        """已经去掉了边距，只包含两行小图的实际宽度"""
        return self.xq_width - self.fun_大图宽度 - self.spacing

    @cached_property
    def fun_小图宽度(self) -> int:
        """去掉了中间边距的小图实际宽度"""
        return math.ceil((self.fun_剩余宽度 - self.spacing) / 2)

    @property
    def fun_左边的大图(self) -> Image.Image:
        im = self.pil_list[0]
        # im = im.resize(
        #     (self.fun_大图宽度, self.xq_height),
        #     resample=Image.Resampling.LANCZOS,
        # )
        im = fun_图片裁剪(im, self.fun_大图宽度, self.xq_height, "center")

        return im

    def main(self) -> Image.Image:
        line_list = []
        right_im_list = []

        ava_ratio = sum([im.width / im.height for im in self.pil_list[1:]]) / len(
            self.pil_list[1:]
        )
        small_height = math.ceil(self.fun_小图宽度 / ava_ratio)

        for im in cycle(self.pil_list[1:]):
            # im = im.resize(
            #     (self.fun_小图宽度, small_height),
            #     resample=Image.Resampling.LANCZOS,
            # )
            print(self.fun_小图宽度, small_height)
            im = fun_图片裁剪(
                im, width=self.fun_小图宽度, height=small_height, position="center"
            )

            line_list.append(im.copy())

            if self.fun_计算单行高度(im_list=line_list) > self.xq_height:
                line_im = fun_图片竖向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )

                right_im_list.append(line_im)

                line_list = []

            if len(right_im_list) == 2:
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

        bg = bg.crop((0, 0, self.xq_width, self.xq_height))

        return bg
