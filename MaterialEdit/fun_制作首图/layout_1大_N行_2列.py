from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片扩大粘贴,
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
    fun_图片边框圆角,
)

from .class_layout_init import LayoutInit


class Layout1大N行2列(LayoutInit):
    @property
    def small_height(self) -> int:
        return int((self.xq_height - (self.spacing * (self.col + 3))) / (self.col + 2))

    @property
    def small_width(self) -> int:
        return int((self.xq_width - (self.spacing * 3)) / 2)

    def first_im(self) -> Image.Image:
        im = fun_图片裁剪(
            im=self.pil_list[0],
            width=int(self.xq_width - (self.spacing * 2)),
            height=int((self.small_height * 2) + self.spacing),
            position="center",
        )

        if self.spacing > 0:
            im = fun_图片边框圆角(im)

        return im

    def main(self):
        line_small_im_list = []
        bottom_im_list = []

        for im in self.pil_list[1:]:
            im = fun_图片裁剪(
                im=im,
                width=self.small_width,
                height=self.small_height,
                position="center",
            )

            if self.spacing > 0:
                im = fun_图片边框圆角(im)

            line_small_im_list.append(im)

            if len(line_small_im_list) == 2:
                line_im = fun_图片横向拼接(
                    image_list=line_small_im_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )

                bottom_im_list.append(line_im)

                line_small_im_list = []

            if len(bottom_im_list) == self.col:
                bottom_im = fun_图片竖向拼接(
                    image_list=bottom_im_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 255),
                )

                break

        bg = fun_图片竖向拼接(
            image_list=[self.first_im(), bottom_im],
            spacing=self.spacing,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )

        return bg
