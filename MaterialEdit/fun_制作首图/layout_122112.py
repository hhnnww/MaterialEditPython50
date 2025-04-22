import math

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit


class Layout122112(LayoutInit):
    @property
    def small_size(self) -> tuple[int, int]:
        """小图的大小"""
        return math.floor((self.xq_width - ((3 + 1) * self.spacing)) / 3), math.floor(
            (self.xq_height - ((5 + 1) * self.spacing)) / 6,
        )

    @property
    def large_size(self) -> tuple[int, int]:
        """大图的大小"""
        return self.small_size[0] * 2 + self.spacing, self.small_size[
            1
        ] * 2 + self.spacing

    @property
    def first_ling(self) -> Image.Image:
        """第一行的图片"""
        return ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        self._pil_list[0],
                        self.large_size,
                        "center",
                    ),
                    self.image_radio,
                ),
                ImageAction.fun_图片竖向拼接(
                    image_list=[
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[1],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[2],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                    ],
                    spacing=self.spacing,
                    align="center",
                ),
            ],
            spacing=self.spacing,
            align="center",
        )

    @property
    def two_line(self) -> Image.Image:
        """第二行的图片"""
        return ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片竖向拼接(
                    image_list=[
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[3],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[4],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                    ],
                    spacing=self.spacing,
                    align="center",
                ),
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        self._pil_list[5],
                        self.large_size,
                        "center",
                    ),
                    self.image_radio,
                ),
            ],
            spacing=self.spacing,
            align="center",
        )

    @property
    def three_line(self) -> Image.Image:
        """第一行的图片"""
        return ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        self._pil_list[6],
                        self.large_size,
                        "center",
                    ),
                    self.image_radio,
                ),
                ImageAction.fun_图片竖向拼接(
                    image_list=[
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[7],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                        ImageAction.fun_图片添加圆角(
                            ImageAction.fun_图片裁剪(
                                self._pil_list[8],
                                self.small_size,
                                "center",
                            ),
                            self.image_radio,
                        ),
                    ],
                    spacing=self.spacing,
                    align="center",
                ),
            ],
            spacing=self.spacing,
            align="center",
        )

    def main(self) -> Image.Image:
        """制作首图"""
        bg = ImageAction.fun_图片竖向拼接(
            image_list=[
                self.first_ling,
                self.two_line,
                self.three_line,
            ],
            spacing=self.spacing,
            align="center",
        )
        bg = ImageAction.fun_图片扩大(
            bg,
            (self.xq_width, self.xq_height),
            Align.CENTER,
            Align.CENTER,
        )
        self.fun_储存design_image(bg)
        return bg
