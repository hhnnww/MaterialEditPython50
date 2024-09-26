import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
)

from .class_layout_init import LayoutInit


class Layout行自适应(LayoutInit):
    @cached_property
    def fun_小图高度(self) -> int:
        return math.ceil((self.xq_height - ((self.col - 1) * self.spacing)) / self.col)

    def fun_计算行宽(self, im_list: list[Image.Image]) -> int:
        return sum([im.width for im in im_list]) + ((len(im_list) - 1) * self.spacing)

    def main(self):
        line_list = []
        bg_list = []
        pil_list = self.pil_list
        pil_list.sort(key=lambda k: k.width / k.height, reverse=True)

        new_list = []

        num = 0
        while True:
            # if len(new_list) == len(pil_list) - 1:
            #     break

            if num == math.ceil(len(pil_list) / 2):
                break

            print(num)
            new_list.append(pil_list[num])
            if num > 0:
                new_list.append(pil_list[0 - num])

            num += 1

        for im in cycle(new_list):
            small_width = math.ceil(self.fun_小图高度 * (im.width / im.height))

            # im = fun_图片裁剪(
            #     im, width=small_width, height=self.fun_小图高度, position="center"
            # )

            im = im.resize(
                (small_width, self.fun_小图高度), resample=Image.Resampling.LANCZOS
            )

            line_list.append(im.copy())

            if self.fun_计算行宽(im_list=line_list) >= self.xq_width * 0.8:
                line_im = fun_图片横向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="start",
                    background_color=(255, 255, 255, 0),
                )
                line_im.thumbnail(
                    (self.xq_width, self.fun_小图高度),
                    resample=Image.Resampling.LANCZOS,
                )
                line_im = line_im.resize(
                    (self.xq_width, self.fun_小图高度),
                    resample=Image.Resampling.LANCZOS,
                )
                bg_list.append(line_im)
                line_list = []

            if len(bg_list) == self.col:
                break

        bg = fun_图片竖向拼接(
            image_list=bg_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 0),
        )

        # bg.thumbnail((self.xq_width, self.xq_height), resample=Image.Resampling.LANCZOS)

        # bg = fun_图片扩大粘贴(
        #     im=bg,
        #     width=self.xq_width,
        #     height=self.xq_height,
        #     left="center",
        #     top="center",
        #     background_color=(255, 255, 255, 0),
        # )

        return bg
