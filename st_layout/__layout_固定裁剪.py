"""固定裁剪布局"""

import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from st_layout.__layout_init import LayoutInit


class Layout固定裁剪(LayoutInit):
    @cached_property
    def __fun_单行行高(self) -> int:
        """行高"""
        if self.has_out_spacing:
            return math.floor(
                (self.xq_height - ((self.col + 1) * self.spacing)) / self.col,
            )

        return math.floor(
            (self.xq_height - ((self.col - 1) * self.spacing)) / self.col,
        )

    @cached_property
    def __fun_根据平均比例计算小图宽度(self) -> float:
        """根据平均比例计算小图宽度"""
        return self.fun_平均图片比例 * self.__fun_单行行高

    @cached_property
    def __fun_计算合适的单行图片数量(self) -> int:
        """计算合适的单行图片数量"""
        return int(self.xq_width / self.__fun_根据平均比例计算小图宽度)

    @cached_property
    def __fun_计算小图宽度(self) -> int:
        """计算小图宽度"""
        if self.has_out_spacing:
            return math.floor(
                (
                    self.xq_width
                    - ((self.__fun_计算合适的单行图片数量 + 1) * self.spacing)
                )
                / self.__fun_计算合适的单行图片数量,
            )
        return math.floor(
            (self.xq_width - ((self.__fun_计算合适的单行图片数量 - 1) * self.spacing))
            / self.__fun_计算合适的单行图片数量,
        )

    def fun_图片固定裁剪(self) -> Image.Image:
        """主函数"""
        line = []
        rows = []
        for pil in cycle(self.fun_所有图片):
            line.append(
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        pil,
                        (self.__fun_计算小图宽度, self.__fun_单行行高),
                        "center",
                    ),
                    self.radio,
                ),
            )
            if len(line) == self.__fun_计算合适的单行图片数量:
                rows.append(ImageAction.fun_图片横向拼接(line, self.spacing, "center"))
                line = []
                if len(rows) == self.col:
                    break

        bg = ImageAction.fun_图片竖向拼接(rows, self.spacing, "start")

        if self.has_out_spacing:
            bg = ImageAction.fun_图片扩大(
                bg,
                (self.xq_width, self.xq_height),
                Align.CENTER,
                Align.CENTER,
            )
        else:
            bg = bg.resize(
                (self.xq_width, self.xq_height),
                Image.Resampling.LANCZOS,
            )
        return ImageAction.fun_图片添加背景(
            bg,
            self.fun_背景颜色,
        )


if __name__ == "__main__":
    from pathlib import Path

    image_list = list(Path(r"F:\小夕素材\11000-11999\11229\11229").glob("*.jpg"))
    gd = Layout固定裁剪(image_list)
    gd.bg_color = "#fff"
    gd.radio = 0
    gd.col = 3
    gd.spacing = 0
    gd.has_out_spacing = True
    gd.fun_图片固定裁剪().show()
