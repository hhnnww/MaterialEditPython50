"""layout init"""

from __future__ import annotations

import math
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from tqdm import tqdm

if TYPE_CHECKING:
    from MaterialEdit.type import ALIGNITEM, ImageModel


class LayoutInit:
    def __init__(
        self,
        image_list: list[ImageModel],
        xq_width: int,
        xq_height: int,
        spacing: int,
        col: int,
        crop_position: ALIGNITEM,
        bg_color: tuple,
        out_space: bool,
        radio: bool,
        design_path: str,
        resize: str = "缩放",
    ) -> None:
        """图片布局初始化."""
        self.design_path = design_path
        self.image_list = image_list
        self.xq_width = xq_width
        self.xq_height = xq_height
        self.spacing = spacing
        self.design_path = design_path

        self.col = col
        self.crop_position: ALIGNITEM = crop_position
        self.bg_color = bg_color
        self.out_space = out_space
        self.resize = resize
        self.radio = radio

    @property
    def image_radio(self) -> int:
        """Image raio"""
        if self.radio:
            return 20
        return 0

    @cached_property
    def _pil_list(self) -> list[Image.Image]:
        pil_list = []
        max_radio = 6
        for image in tqdm(self.image_list, desc="制作首图布局", ncols=100):
            im = Image.open(image.path)
            if im.mode.lower() != "rgba":
                im = im.convert("RGBA")

            if im.height / im.width > max_radio:
                im = im.crop((0, 0, im.width, im.width * max_radio))

            pil_list.append(im)

            max_pic_count = 50
            if len(pil_list) >= max_pic_count:
                break

        return pil_list

    @staticmethod
    def _fun_打开图片(image_path: str) -> Image.Image:
        im = Image.open(image_path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")
        return im

    @cached_property
    def _fun_所有图片平均比例(self) -> float:
        return sum([im.width / im.height for im in self._pil_list]) / len(
            self._pil_list,
        )

    @staticmethod
    def _fun_计算小图高度(im: Image.Image, ori_width: int) -> int:
        return math.ceil(ori_width / (im.width / im.height))

    def _fun_计算单行高度(self, im_list: list[Image.Image]) -> int:
        return sum([im.height for im in im_list]) + ((len(im_list) - 1) * self.spacing)

    def _fun_计算单行宽度(self, im_list: list[Image.Image]) -> int:
        return sum([im.width for im in im_list]) + ((len(im_list) - 1) * self.spacing)

    def fun_储存design_image(self, im: Image.Image) -> None:
        """保存设计图像"""
        design_path_obj = Path(self.design_path)
        if design_path_obj.exists() is not True:
            design_path_obj.mkdir(parents=True, exist_ok=True)

        png_path = design_path_obj / f"{len(list(design_path_obj.iterdir()))}.png"
        im.save(png_path)
