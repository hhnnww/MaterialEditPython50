"""制作详情"""

from __future__ import annotations

import math
from functools import cached_property
from typing import TYPE_CHECKING, Literal

from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.get_stem_num import get_path_num
from MaterialEdit.router_制作详情2.class_单个图片 import ClassOneImage
from MaterialEdit.setting import MATERIAL_SOURCE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path

Image.MAX_IMAGE_PIXELS = None


class ClassMakeXQ2:
    """制作素材详情"""

    def __init__(
        self,
        image_list: list[Path],
        col: int,
        shop_name: str,
        has_name: bool,
        use_pic: int,
        pic_sort: bool,
        material_path: Path,
        has_water: bool,
        oneline_ratio: float,
        effect_has_watermark: bool,
    ) -> None:
        """初始化."""
        self.col = col
        self.shop_name = shop_name
        self.has_name = has_name

        self.use_pic = use_pic
        self.pic_sort = pic_sort

        self.material_path = material_path
        self.has_water = has_water
        self.oneline_ratio = oneline_ratio
        self.effect_has_watermark = effect_has_watermark

        self.image_list_path = self.__fun_获取仅使用的图片(image_list=image_list)
        self.image_list = self.__fun_排序图片(image_list=self.image_list_path)

    xq_width = 2000
    space = 40
    background_color = (255, 255, 255, 255)

    @cached_property
    def __fun_所有源文件(self) -> list[Path]:
        """构建所有源文件"""
        return rglob(
            folder=self.material_path.as_posix(),
            suffix=MATERIAL_SOURCE_SUFFIX,
        )

    def __fun_获取仅使用的图片(self, image_list: list[Path]) -> list[Path]:
        if self.pic_sort:
            image_list.sort(key=lambda k: get_path_num(stem=k.stem), reverse=False)
        else:
            image_list.sort(key=lambda k: get_path_num(stem=k.stem), reverse=True)

        if self.use_pic == 0:
            return image_list

        return image_list[: self.use_pic]

    def __fun_排序图片(self, image_list: list[Path]) -> list[ClassOneImage]:
        obj_list: list[ClassOneImage] = []
        max_size = 20
        for image in tqdm(image_list, desc="加载图片", ncols=100):
            size = image.stat().st_size / 1000 / 1000
            if size > max_size:
                continue

            opim = Image.open(fp=image.as_posix())
            opim.thumbnail((1500, 99999), Image.Resampling.LANCZOS)
            obj_list.append(
                ClassOneImage(
                    image_pil=opim,
                    image_path=image,
                    image_width=800,
                    background_color=self.background_color,
                    shop_name=self.shop_name,
                    has_name=self.has_name,
                    all_material_file=self.__fun_所有源文件,
                    has_water=self.has_water,
                    effect_has_watermark=self.effect_has_watermark,
                ),
            )

        if self.col == 1:
            return obj_list

        obj_list.sort(key=lambda k: k.fun_图片比例, reverse=True)

        return obj_list

    def __fun_制作单行(self, image_list: list[ClassOneImage]) -> Image.Image:
        width = math.floor(
            (self.xq_width - ((len(image_list) - 1) * self.space)) / len(image_list),
        )

        im_list = []
        for image in image_list:
            image.image_width = width
            im_list.append(image.main())

        im = fun_图片横向拼接(
            image_list=im_list,
            spacing=self.space,
            align_item="end",
            background_color=self.background_color,
        )

        return fun_图片扩大粘贴(
            im=im,
            width=self.xq_width,
            height=im.height,
            left="center",
            top="center",
            background_color=self.background_color,
        )

    def __计算单行图片的比例(
        self,
        online_comb: list[ClassOneImage],
    ) -> float | Literal[0]:
        return sum([comb.fun_图片比例 for comb in online_comb])

    @cached_property
    def __fun_组合图片列表(self) -> list[list[ClassOneImage]]:
        image_list = []
        in_list = []

        for num, image in enumerate(iterable=self.image_list):
            in_list.append(image)

            next_list = in_list
            if num < len(self.image_list) - 1:
                next_list = [*in_list, self.image_list[num + 1]]

            if (
                len(in_list) == self.col
                or self.__计算单行图片的比例(online_comb=next_list)
                >= self.oneline_ratio
                or (num + 1 == len(self.image_list) and len(in_list) > 0)
            ):
                image_list.append(in_list.copy())
                in_list = []

        return image_list

    def main(self) -> Image.Image:
        """开始执行制作详情"""
        im_list = [
            self.__fun_制作单行(image_list=line_image)
            for line_image in tqdm(self.__fun_组合图片列表, desc="制作详情", ncols=100)
        ]

        spacing = 0 if self.has_name else self.space

        bg = fun_图片竖向拼接(
            image_list=im_list,
            spacing=spacing,
            align_item="center",
            background_color=self.background_color,
        )

        return fun_图片扩大粘贴(
            im=bg,
            width=2060,
            height=bg.height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )
