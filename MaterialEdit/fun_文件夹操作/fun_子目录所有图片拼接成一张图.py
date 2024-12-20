"""拼接子目录内的所有图片."""

from __future__ import annotations

import math
import re
from functools import cached_property
from itertools import cycle
from pathlib import Path

import tqdm
from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.setting import IMAGE_SUFFIX


class MergeSinglePath:
    """拼接单个目录."""

    def __init__(self, sub_path: Path, row: int, col: int) -> None:
        """输入子目录路径和后面图片的栏数."""
        self.sub_path = sub_path
        self.row = row
        self.col = col

        self._all_images: list[Path] = [
            image
            for image in self.sub_path.iterdir()
            if image.is_file() and image.suffix.lower() in IMAGE_SUFFIX
        ]

        self.sort_all_images()

    spacing = 16
    background_color = (255, 255, 255, 255)

    @staticmethod
    def get_num(stem: str) -> int:
        """获取stem中的数字."""
        num_list = re.findall(r"\d+", stem)
        if len(num_list) == 0:
            return 0
        return int("".join(num_list))

    @property
    def all_images(self) -> list[Path]:
        """子目录内的所有图片."""
        return self._all_images

    def sort_all_images(self) -> None:
        """设置新的列表."""
        self._all_images.sort(key=lambda k: self.get_num(stem=k.stem), reverse=False)

    @cached_property
    def all_pil(self) -> list[Image.Image]:
        """打开所有图片."""
        return [Image.open(image.as_posix()).convert("RGBA") for image in self.all_images]

    @cached_property
    def first_pil(self) -> Image.Image:
        """第一张图片."""
        return self.all_pil[0].copy()

    @property
    def last_pil(self) -> Image.Image:
        """后面的图片."""
        width = math.floor((self.first_pil.width - self.spacing) / 2)

        in_list: list[Image.Image] = []
        comb_list: list[Image.Image] = []
        for pil in tqdm.tqdm(cycle(self.all_pil[1:]), ncols=100, desc="制作画册大图"):
            im = pil.copy()
            im.thumbnail((width, 999999))
            in_list.append(im)

            if len(in_list) == self.row:
                in_list_pil = fun_图片横向拼接(
                    image_list=in_list,
                    spacing=self.spacing,
                    align_item="start",
                    background_color=self.background_color,
                )
                in_list = []
                comb_list.append(in_list_pil)

            if len(comb_list) == self.col:
                return fun_图片竖向拼接(
                    image_list=comb_list,
                    spacing=self.spacing,
                    align_item="center",
                    background_color=self.background_color,
                )

        return Image.new("RGBA", (10, 10), self.background_color)

    def main(self) -> Image.Image:
        """开始拼接图片."""
        im = fun_图片竖向拼接(
            image_list=[self.first_pil, self.last_pil],
            spacing=self.spacing,
            align_item="center",
            background_color=self.background_color,
        )
        return fun_图片扩大粘贴(
            im=im,
            width=im.width + (self.spacing * 2),
            height=im.height + (self.spacing * 2),
            left="center",
            top="center",
            background_color=self.background_color,
        )


class MergeSubPathImages:
    """拼接子目录内的所有图片为一张图."""

    row = 2
    col = 3

    def __init__(self, material_path_str: str) -> None:
        """输入素材文件夹目录."""
        self.material_path = Path(material_path_str)

    @property
    def all_sub_path(self) -> list[MergeSinglePath]:
        """所有子目录."""
        return [
            MergeSinglePath(
                sub_path=sub_path,
                row=self.row,
                col=self.col,
            )
            for sub_path in self.material_path.iterdir()
            if sub_path.is_dir()
        ]

    def main(self) -> None:
        """开始给每个子目录制作图片 并且删除所有图片."""
        for obj in self.all_sub_path:
            im = obj.main()

            for image in obj.all_images:
                image.unlink()

            image_path = obj.sub_path / f"{obj.sub_path.stem}.png"
            im.save(image_path)


if __name__ == "__main__":
    MergeSubPathImages(material_path_str=r"F:\小夕素材\10000-20000\10961\10961").main()
