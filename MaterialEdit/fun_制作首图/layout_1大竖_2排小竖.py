from functools import cached_property

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片扩大粘贴,
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片边框圆角,
)

from .class_layout_init import LayoutInit


class Layout1大竖2排小竖(LayoutInit):
    @cached_property
    def fun_大图宽度(self) -> int:
        """去掉边距后的大图实际宽度"""
        im = self.pil_list[0]
        dst_height = self.xq_height - (self.spacing * 2)
        return int(dst_height * (im.width / im.height))

    @cached_property
    def fun_剩余宽度(self) -> int:
        """已经去掉了边距，只包含两行小图的实际宽度"""
        return self.xq_width - self.fun_大图宽度 - (self.spacing * 3)

    @cached_property
    def fun_小图宽度(self) -> int:
        """去掉了中间边距的小图实际宽度"""
        return int((self.fun_剩余宽度 - self.spacing) / 2)

    @property
    def fun_左边的大图(self) -> Image.Image:
        im = self.pil_list[0]
        im = im.resize(
            (self.fun_大图宽度, self.xq_height - (self.spacing * 2)),
            resample=Image.Resampling.LANCZOS,
        )

        if self.spacing > 0:
            im = fun_图片边框圆角(im)

        return im

    def main(self) -> Image.Image:
        pil_list = self.pil_list[1:] + self.pil_list[1:] + self.pil_list[1:]

        line_list = []
        right_im_list = []
        for im in pil_list:
            im = im.resize(
                (
                    self.fun_小图宽度,
                    self.fun_计算小图高度(im=im, ori_width=self.fun_小图宽度),
                ),
                resample=Image.Resampling.LANCZOS,
            )

            if self.spacing > 0:
                im = fun_图片边框圆角(im)

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

        bg = bg.crop((0, 0, bg.width, self.xq_height - self.spacing))

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="end",
            background_color=(255, 255, 255, 255),
        )

        return bg
