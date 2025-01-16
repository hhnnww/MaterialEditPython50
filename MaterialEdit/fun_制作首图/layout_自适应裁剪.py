"""自适应裁剪"""

import math
from itertools import combinations

from PIL import Image
from pydantic import BaseModel
from tqdm import tqdm

from MaterialEdit.fun_制作首图.fun_重新构建所有图片 import fun_重新构建所有图片
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.type import ALIGNITEM, ImageModel


class CombList(BaseModel):
    ratio: float
    image_list: list[ImageModel]
    diff: float


class LayoutAdaptiveCrop:
    def __init__(  # noqa: PLR0913
        self,
        image_list: list[ImageModel],
        xq_width: int,
        xq_height: int,
        line: int,
        spacing: int,
        crop_position: ALIGNITEM,
    ) -> None:
        """初始化"""
        self.image_list = fun_重新构建所有图片(image_list)
        self.xq_width = xq_width
        self.xq_height = xq_height
        self.line = line
        self.spacing = spacing - 4
        self.crop: ALIGNITEM = crop_position

        self.online_height = int(
            (self.xq_height - ((self.line + 1) * self.spacing)) / self.line,
        )

    def fun_构建所有组合(self) -> list[CombList]:
        """构建所有组合"""
        oneline_ratio = self.fun_计算单行比例()
        comb_image_list = []
        for x in range(1, 6):
            for in_line in combinations(self.image_list, x):
                ratio = sum([obj.ratio for obj in in_line])
                comb_image_list.append(
                    CombList(
                        image_list=list(in_line),
                        ratio=ratio,
                        diff=abs(oneline_ratio - ratio),
                    ),
                )

        comb_image_list.sort(key=lambda k: k.diff, reverse=False)
        return comb_image_list

    def fun_计算单行比例(self) -> float:
        """计算比例"""
        online_height = math.ceil(
            (self.xq_height - ((self.line + 1) * self.spacing)) / self.line,
        )
        return self.xq_width / online_height

    def fun_构建首图组合(self) -> list[CombList]:
        """构建首图组合"""
        used_comb_list = []
        used_image = []

        for comb_list in self.fun_构建所有组合():
            comb_used = False
            for in_item in comb_list.image_list:
                if in_item.path in used_image:
                    comb_used = True

            if not comb_used:
                used_comb_list.append(comb_list)
                used_image.extend([in_item.path for in_item in comb_list.image_list])

            if len(used_comb_list) == self.line:
                break

        return used_comb_list

    def fun_制作单行(self, comb_list: CombList) -> Image.Image:
        """制作单行"""
        all_pil = []
        col_width = math.ceil(
            (self.xq_width - ((len(comb_list.image_list) + 1) * self.spacing))
            / sum([obj.ratio for obj in comb_list.image_list]),
        )
        for image in comb_list.image_list:
            im = Image.open(image.path)
            im = fun_图片裁剪(
                im,
                math.ceil(col_width * image.ratio),
                self.online_height,
                self.crop,
            )

            all_pil.append(im)

        return fun_图片横向拼接(all_pil, self.spacing, "center", (255, 255, 255, 255))

    def run_制作自适应布局图片(self) -> Image.Image:
        """制作自适应布局图片"""
        all_pil = [
            self.fun_制作单行(comb_list)
            for comb_list in tqdm(self.fun_构建首图组合(), ncols=100, desc="制作首图\t")
        ]

        bg = fun_图片竖向拼接(all_pil, self.spacing, "start", (255, 255, 255, 255))

        return fun_图片扩大粘贴(
            bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )
