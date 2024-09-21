from functools import cached_property

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片扩大粘贴,
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
    fun_图片边框圆角,
)

from .class_layout_init import LayoutInit


class Layout1大N行自适应(LayoutInit):
    @cached_property
    def first_image(self) -> Image.Image:
        im = self.pil_list[0]
        first_width = int(self.xq_width - (self.spacing * 2))
        first_height = int(
            (self.xq_width - (self.spacing * 2)) / (im.width / im.height)
        )
        im = im.resize((first_width, first_height), resample=Image.Resampling.LANCZOS)

        if self.spacing > 0:
            im = fun_图片边框圆角(im)

        return im

    @cached_property
    def bottom_height(self) -> int:
        return self.xq_height - (self.spacing * 2) - self.first_image.height

    @cached_property
    def small_width(self) -> int:
        return int((self.xq_width - (self.spacing * 3)) / 2)

    def main(self):
        col_list = []
        bottom_list = []
        for pil in self.pil_list[1:]:
            small_height = int(self.small_width / (pil.width / pil.height))
            im = pil.resize(
                (self.small_width, small_height), resample=Image.Resampling.LANCZOS
            )

            if self.spacing > 0:
                im = fun_图片边框圆角(im)

            col_list.append(im)

            col_height = sum([in_pil.height for in_pil in col_list]) + (
                (len(col_list) - 1) * self.spacing
            )

            if col_height >= self.bottom_height:
                col_im = fun_图片竖向拼接(
                    image_list=col_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )
                bottom_list.append(col_im)
                col_list = []

            if len(bottom_list) == 2:
                break

        bottom_im = fun_图片横向拼接(
            image_list=bottom_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片竖向拼接(
            image_list=[self.first_image, bottom_im],
            spacing=self.spacing,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片裁剪(
            im=bg,
            width=bg.width,
            height=self.xq_height - self.spacing,
            position="start",
        )

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="end",
            background_color=(255, 255, 255, 255),
        )

        return bg
