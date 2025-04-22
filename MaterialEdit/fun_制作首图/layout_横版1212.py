"""文件重命名.py"""

import math

from PIL import Image

from image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_制作首图.layout_1大3小_自适应 import LayoutInit


class Layout1212(LayoutInit):
    @property
    def small_width(self) -> int:
        """计算小图宽度."""
        if self.radio:
            return math.ceil((self.xq_width - (self.spacing * 4)) / 3)

        return math.ceil((self.xq_width - (self.spacing * 2)) / 3)

    @property
    def small_height(self) -> int:
        """计算小图高度."""
        if self.radio:
            return math.ceil((self.xq_height - (self.spacing * 5)) / 4)

        return math.ceil((self.xq_height - (self.spacing * 3)) / 4)

    def main(self) -> Image.Image:
        """开始制作首图."""
        # 第一张大图
        first_line = ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        self._pil_list[0],
                        (
                            self.small_width * 2 + self.spacing,
                            self.small_height * 2 + self.spacing,
                        ),
                        "center",
                    ),
                    self.image_radio,
                ),
                ImageAction.fun_图片竖向拼接(
                    [
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                pil,
                                (self.small_width, self.small_height),
                                "center",
                            ),
                            self.image_radio,
                        )
                        for pil in self._pil_list[1:3]
                    ],
                    spacing=self.spacing,
                    align="start",
                ),
            ],
            spacing=self.spacing,
            align="center",
        )
        # 第二行
        second_line = ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        self._pil_list[3],
                        (
                            self.small_width * 2 + self.spacing,
                            self.small_height * 2 + self.spacing,
                        ),
                        "center",
                    ),
                    self.image_radio,
                ),
                ImageAction.fun_图片竖向拼接(
                    [
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                pil,
                                (self.small_width, self.small_height),
                                "center",
                            ),
                            self.image_radio,
                        )
                        for pil in self._pil_list[4:6]
                    ],
                    spacing=self.spacing,
                    align="start",
                ),
            ],
            spacing=self.spacing,
            align="start",
        )

        return ImageAction.fun_图片添加背景(
            ImageAction.fun_图片扩大(
                ImageAction.fun_图片竖向拼接(
                    image_list=[first_line, second_line],
                    spacing=self.spacing,
                    align="start",
                ),
                (self.xq_width, self.xq_height),
                Align.CENTER,
                Align.CENTER,
            ),
            self.bg_color,
        )
