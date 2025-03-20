"""行自适应和固定尺寸首图"""

import math
from functools import cached_property
from itertools import cycle
from typing import Literal

from PIL import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class Layout行自适应(LayoutInit):
    @cached_property
    def __fun_小图高度(self) -> int:
        if self.out_space is True:
            return math.floor(
                (self.xq_height - ((self.col + 1) * self.spacing)) / self.col,
            )

        return math.floor((self.xq_height - ((self.col - 1) * self.spacing)) / self.col)

    @cached_property
    def __fun_固定尺寸小图宽度(self) -> int:
        return math.floor(self.__fun_小图高度 * self._fun_所有图片平均比例)

    def main(self, small_size: Literal["固定尺寸", "自适应"]) -> Image.Image:
        """根据给定的图片列表生成一个拼接后的图像。

        参数:
            small_size (Literal["固定尺寸", "自适应"]): 指定小图的处理方式。
                - "固定尺寸": 将小图裁剪为固定尺寸。
                - "自适应": 根据高度自适应调整小图宽度。
        返回:
            Image.Image: 拼接后的图像。
        功能描述:
            1. 遍历图片列表，根据 small_size 参数对每张图片进行处理：
                - 如果为 "自适应"，调整图片宽度以保持比例。
                - 如果为 "固定尺寸"，裁剪图片为指定的固定尺寸。
            2. 将处理后的图片逐行拼接，当单行宽度达到指定值时，生成一行图像。
            3. 当达到指定的行数时，停止处理。
            4. 将所有行图像竖向拼接为最终图像。
            5. 对最终图像进行裁剪和调整大小以符合目标尺寸。
        """
        line_list = []
        bg_list = []

        for image in cycle(self.image_list):
            im = self._fun_打开图片(image_path=image.path)

            if small_size == "自适应":
                small_width = math.floor(self.__fun_小图高度 * (im.width / im.height))
                im = im.resize(
                    (small_width, self.__fun_小图高度),
                    resample=Image.Resampling.LANCZOS,
                )

            elif small_size == "固定尺寸":
                im = fun_图片裁剪(
                    im=im,
                    width=self.__fun_固定尺寸小图宽度,
                    height=self.__fun_小图高度,
                    position=self.crop_position,
                )

            line_list.append(im.copy())

            if self._fun_计算单行宽度(im_list=line_list) >= self.xq_width:
                line_im = fun_图片横向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.bg_color,
                )
                line_list = []

                bg_list.append(line_im.copy())

            if len(bg_list) == self.col:
                break

        bg = fun_图片竖向拼接(
            image_list=bg_list,
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        crop_left = math.floor((bg.width - self.xq_width) / 2)
        bg = bg.crop((crop_left, 0, self.xq_width + crop_left, bg.height))

        return bg.resize((self.xq_width, self.xq_height + 1), Image.Resampling.LANCZOS)
