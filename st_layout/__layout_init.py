"""布局初始化类."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from PIL import Image, ImageColor
from tqdm import tqdm

if TYPE_CHECKING:
    from pathlib import Path


class LayoutInit:
    """布局初始化类"""

    spacing = 10
    has_out_spacing = True
    radio = 0
    xq_width = 1500
    xq_height = 1500
    col = 4
    bg_color = "#FFFFFF"

    def __init__(self, image_file_list: list[str] | list[Path]) -> None:
        """初始化函数"""
        self.image_file_list = image_file_list

    @cached_property
    def fun_背景颜色(
        self,
    ) -> tuple[int, int, int, int]:
        """背景颜色"""
        rgb_color = ImageColor.getrgb(self.bg_color)
        return int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]), 255

    @cached_property
    def fun_所有图片(self) -> tqdm[Image.Image]:
        """所有图片"""
        return tqdm(
            [
                Image.open(image_file).convert("RGBA")
                for image_file in self.image_file_list
            ],
            desc="制作首图 加载图片",
        )

    @cached_property
    def fun_平均图片比例(self) -> float:
        """平均图片比例"""
        return sum(
            [image.size[0] / image.size[1] for image in self.fun_所有图片],
        ) / len(self.fun_所有图片)
