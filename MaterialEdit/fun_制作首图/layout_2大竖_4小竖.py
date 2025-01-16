"""Module provides the Layout2大竖4小竖 class for creating a specific image layout.

This layout consists of two large vertical images and four small vertical images.
"""

import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片竖向拼接, fun_图片裁剪


class Layout2大竖4小竖(LayoutInit):
    MAX_BOTTOM_IMAGES = 4

    @cached_property
    def fun_顶部图片(self) -> Image.Image:
        """Create the top image of the layout."""
        im_width = math.ceil((self.xq_width - self.spacing) / 2)
        im_height = math.ceil(im_width / self._fun_所有图片平均比例)
        return fun_图片横向拼接(
            image_list=[
                fun_图片裁剪(
                    im=self._pil_list[0],
                    width=im_width,
                    height=im_height,
                    position="center",
                ),
                fun_图片裁剪(
                    im=self._pil_list[1],
                    width=im_width,
                    height=im_height,
                    position="center",
                ),
            ],
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

    def fun_底部图片(self) -> Image.Image:
        """Create the bottom image of the layout."""
        im_width = math.ceil((self.xq_width - (self.spacing * 3)) / 4)
        im_height = math.ceil(im_width / self._fun_所有图片平均比例)
        bottom_height = self.xq_height - self.fun_顶部图片.height - self.spacing

        line_image_list = []
        bottom_image_list = []

        for im in cycle(self._pil_list[2:]):
            cropped_im = fun_图片裁剪(
                im=im,
                width=im_width,
                height=im_height,
                position="center",
            )
            line_image_list.append(cropped_im.copy())

            if self._fun_计算单行高度(line_image_list) >= bottom_height:
                bottom_im = fun_图片竖向拼接(
                    image_list=line_image_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )
                bottom_image_list.append(bottom_im.copy())

                line_image_list = []

            if len(bottom_image_list) == self.MAX_BOTTOM_IMAGES:
                break

        bg = fun_图片横向拼接(
            image_list=bottom_image_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片竖向拼接(
            image_list=[self.fun_顶部图片, bg],
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        return bg.crop((0, 0, self.xq_width, self.xq_height))
