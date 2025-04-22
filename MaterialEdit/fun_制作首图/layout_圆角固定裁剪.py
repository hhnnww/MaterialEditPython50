import math
from itertools import cycle

from PIL.Image import Image
from pydantic import BaseModel

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit


class AbsModel(BaseModel):
    abs: int
    line_num: int


class LayoutRadioCrop(LayoutInit):
    @property
    def small_height(self) -> int:
        """计算小图的高度。"""
        return math.ceil(
            (self.xq_height - (self.spacing * (self.col + 1))) / self.col,
        )

    @property
    def fun_计算最合适的单行列(self) -> int:
        """计算最合适的单行列数。"""
        small_width = self.small_height * self._fun_所有图片平均比例
        return int(self.xq_width / small_width)

    @property
    def fun_计算小图宽度(self) -> int:
        """计算小图的宽度。"""
        return math.ceil(
            (self.xq_width - (self.spacing * (self.fun_计算最合适的单行列 + 1)))
            / self.fun_计算最合适的单行列,
        )

    def main(self) -> Image:
        """主函数，用于生成裁剪和合并后的图片。"""
        rows_list = []
        line_list = []
        for pil in cycle(self._pil_list):
            line_list.append(
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        pil,
                        (self.fun_计算小图宽度, self.small_height),
                        self.crop_position,
                    ),
                    20,
                ),
            )

            if len(line_list) == self.fun_计算最合适的单行列:
                rows_list.append(
                    ImageAction.fun_图片横向拼接(
                        image_list=line_list,
                        spacing=self.spacing,
                        align="center",
                    ).copy(),
                )
                line_list = []

                if len(rows_list) >= self.col:
                    break

        row_bg = ImageAction.fun_图片竖向拼接(
            image_list=rows_list,
            spacing=self.spacing,
            align="start",
        )

        return ImageAction.fun_图片添加背景(
            ImageAction.fun_图片扩大(
                row_bg,
                (self.xq_width, self.xq_height),
                Align.CENTER,
                Align.CENTER,
            ),
            self.bg_color,
        )
