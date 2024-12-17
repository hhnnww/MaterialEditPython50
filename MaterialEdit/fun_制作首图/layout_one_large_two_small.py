"""
一个大行
下面每行2个的小行图片布局
"""

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片扩大粘贴,
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
    fun_图片边框圆角,
)

from .class_layout_init import LayoutInit


class LayoutOneLargeTwoSmall(LayoutInit):
    """第一行占满宽度
    后面每行两个图片

    Args:
        LayoutInit (_type_): _description_

    Returns:
        _type_: _description_
    """

    @property
    def small_height(self) -> int:
        """计算后面小图的高度

        Returns:
            int: _description_
        """
        return int((self.xq_height - (self.spacing * (self.col + 3))) / (self.col + 2))

    @property
    def small_width(self) -> int:
        """计算后面小图的宽度

        Returns:
            int: _description_
        """
        return int((self.xq_width - (self.spacing * 3)) / 2)

    def first_im(self) -> Image.Image:
        """构建第一个大图图片

        Returns:
            Image.Image: _description_
        """
        im = fun_图片裁剪(
            im=self._pil_list[0],
            width=int(self.xq_width - (self.spacing * 2)),
            height=int((self.small_height * 2) + self.spacing),
            position="center",
        )

        # if self.spacing > 0:
        #     im = fun_图片边框圆角(im)

        return im

    def main(self) -> Image.Image:
        """开始组合图片

        Returns:
            _type_: _description_
        """
        line_small_im_list = []
        bottom_im_list = []

        for im in self._pil_list[1:]:
            im = fun_图片裁剪(
                im=im,
                width=self.small_width,
                height=self.small_height,
                position="center",
            )

            if self.spacing > 0:
                im = fun_图片边框圆角(im=im)

            line_small_im_list.append(im)

            if len(line_small_im_list) == 2:
                line_im = fun_图片横向拼接(
                    image_list=line_small_im_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.bg_color,
                )

                bottom_im_list.append(line_im)

                line_small_im_list = []

            if len(bottom_im_list) == self.col:
                bottom_im = fun_图片竖向拼接(
                    image_list=bottom_im_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.bg_color,
                )

                break

        bg = fun_图片竖向拼接(
            image_list=[self.first_im(), bottom_im],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="center",
            background_color=self.bg_color,
        )

        return bg
