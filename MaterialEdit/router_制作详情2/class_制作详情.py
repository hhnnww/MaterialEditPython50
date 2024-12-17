"""制作详情"""

import math
from functools import cached_property
from pathlib import Path
from typing import Literal

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件
from MaterialEdit.fun_获取路径数字 import fun_获取路径数字
from MaterialEdit.router_制作详情2.class_单个图片 import ClassOneImage
from MaterialEdit.setting import MATERIAL_SOURCE_SUFFIX


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
    ) -> None:
        self.col = col
        self.shop_name = shop_name
        self.has_name = has_name

        self.use_pic = use_pic
        self.pic_sort = pic_sort

        self.material_path = material_path
        self.has_water = has_water
        self.oneline_ratio = oneline_ratio

        self.image_list = self.__fun_获取仅使用的图片(image_list=image_list)
        self.image_list = self.__fun_排序图片(image_list=self.image_list)

    xq_width = 2000
    space = 8
    background_color = (255, 255, 255, 255)

    @cached_property
    def __fun_所有源文件(self) -> list[Path]:
        return fun_遍历指定文件(
            folder=self.material_path.as_posix(), suffix=MATERIAL_SOURCE_SUFFIX
        )

    def __fun_获取仅使用的图片(self, image_list: list[Path]) -> list[Path]:
        if self.pic_sort:
            image_list.sort(key=lambda k: fun_获取路径数字(stem=k.stem), reverse=False)
        else:
            image_list.sort(key=lambda k: fun_获取路径数字(stem=k.stem), reverse=True)

        if self.use_pic == 0:
            return image_list

        return image_list[: self.use_pic]

    def __fun_排序图片(self, image_list: list[Path]) -> list[ClassOneImage]:
        obj_list = [
            ClassOneImage(
                image_pil=Image.open(fp=image.as_posix()),
                image_path=image,
                image_width=800,
                background_color=self.background_color,
                shop_name=self.shop_name,
                has_name=self.has_name,
                all_material_file=self.__fun_所有源文件,
                has_water=self.has_water,
            )
            for image in image_list
        ]
        avatar_ratio = sum([obj.fun_图片比例 for obj in obj_list]) / len(obj_list)
        if avatar_ratio < 0.2 or self.col == 1:
            return obj_list

        obj_list.sort(key=lambda k: k.fun_图片比例, reverse=True)

        return obj_list

    def __fun_制作单行(self, image_list: list[ClassOneImage]) -> Image.Image:
        print(f"制作单行{image_list}")
        width = math.floor(
            (self.xq_width - ((len(image_list) - 1) * self.space)) / len(image_list)
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

        im = fun_图片扩大粘贴(
            im=im,
            width=self.xq_width,
            height=im.height,
            left="center",
            top="center",
            background_color=self.background_color,
        )

        return im

    def __计算单行图片的比例(
        self, online_comb: list[ClassOneImage]
    ) -> float | Literal[0]:
        return sum([comb.fun_图片比例 for comb in online_comb])

    @cached_property
    def __fun_组合图片列表(self) -> list[list[ClassOneImage]]:
        image_list = []
        in_list = []
        break_num = 0

        for num, image in enumerate(iterable=self.image_list):
            in_list.append(image)

            if (
                (num - break_num > 10 or break_num == 0)
                and len(in_list) == self.col - 1
                or self.__计算单行图片的比例(online_comb=in_list) >= self.oneline_ratio
            ):
                image_list.append(in_list.copy())
                in_list = []
                break_num = num + 1

            elif (num + 1 == len(self.image_list) and len(in_list) > 0) or len(
                in_list
            ) == self.col:
                image_list.append(in_list.copy())
                in_list = []

        return image_list

    def main(self) -> Image.Image:
        """开始执行制作详情

        Returns:
            Image.Image: _description_
        """
        im_list = [
            self.__fun_制作单行(image_list=line_image)
            for line_image in self.__fun_组合图片列表
        ]

        if self.has_name:
            spacing = 0
        else:
            spacing = self.space

        return fun_图片竖向拼接(
            image_list=im_list,
            spacing=spacing,
            align_item="center",
            background_color=self.background_color,
        )
