"""列固定尺寸排版."""

import math
from functools import cached_property
from itertools import cycle
from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_图片横向拼接,
    fun_图片竖向拼接,
    fun_图片裁剪,
)

from .class_layout_init import LayoutInit


class Layout列固定尺寸(LayoutInit):
    """列固定尺寸排版."""

    @cached_property
    def fun_pil_list(self) -> list[Image.Image]:
        """打开所有图片."""
        return [Image.open(image.path) for image in self.image_list]

    @cached_property
    def fun_平均比例(self) -> float:
        """计算所有图片平均比例."""
        return sum([im.width / im.height for im in self.fun_pil_list]) / len(
            self.fun_pil_list,
        )

    @cached_property
    def fun_small_width(self) -> int:
        """小图宽度."""
        return math.ceil((self.xq_width - (self.spacing * (self.col - 1))) / self.col)

    @cached_property
    def fun_small_height(self) -> int:
        """小图高度."""
        return math.ceil(self.fun_small_width / self.fun_平均比例)

    def main(self) -> Image.Image:
        """开始制作图片."""
        line_list = []
        all_list = []
        sm_width = self.fun_small_width
        sm_height = self.fun_small_height

        for im_file in cycle(self.image_list):
            im = Image.open(im_file.path)

            if im.mode.lower() != "rgba":
                im = im.convert("RGBA")

            im = fun_图片裁剪(
                im=im,
                width=sm_width,
                height=sm_height,
                position="center",
            )

            line_list.append(im.copy())

            if self._fun_计算单行高度(im_list=line_list) > self.xq_height:
                line_im = fun_图片竖向拼接(
                    image_list=line_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=(255, 255, 255, 0),
                )
                all_list.append(line_im.copy())

                line_list = []

            if len(all_list) == self.col:
                break

        bg = fun_图片横向拼接(
            image_list=all_list,
            spacing=self.spacing,
            align_item="start",
            background_color=(255, 255, 255, 0),
        )

        if Path(self.design_path).exists() is not True:
            Path(self.design_path).mkdir()

        bg.save(fp=(Path(self.design_path) / "0.png").as_posix())
        return bg.crop((0, 0, self.xq_width, self.xq_height))
