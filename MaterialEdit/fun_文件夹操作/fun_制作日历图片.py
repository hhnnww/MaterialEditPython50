"""制作日历图片."""

from pathlib import Path
from typing import Literal

from PIL import Image
from PIL.ImageFile import ImageFile
from tqdm import tqdm

from MaterialEdit.fun_图片编辑 import fun_图片扩大粘贴, fun_图片竖向拼接, fun_图片裁剪
from MaterialEdit.fun_图片编辑.class_image_edit import (
    fun_图片切换到圆角,
    fun_图片横向拼接,
    fun_图片画边框,
)
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


class MakeCalenderPic:
    def __init__(self, material_path: str) -> None:
        """制作日历图片."""
        self.material_path = Path(material_path)
        self.gutter = 10
        self.width = 750
        self.radio = 10

    @staticmethod
    def fun_判断横竖版本(png_list: list[Image.Image]) -> Literal["h", "s"]:
        """判断横竖版本."""
        ver_ratio = 0.7
        average_ratio = sum([obj.width / obj.height for obj in png_list]) / len(
            png_list,
        )
        if average_ratio > ver_ratio:
            return "h"

        return "s"

    @staticmethod
    def fun_获取文件夹所有图片(sub_path: Path) -> list[ImageFile]:
        """获取文件夹所有图片."""
        png_file_list = [
            Image.open(obj.as_posix())
            for obj in rglob(folder=sub_path.as_posix(), suffix=[".png"])
        ]
        png_file_list.sort(key=lambda k: k.width / k.height, reverse=True)

        return png_file_list

    @staticmethod
    def fun_图片列表编组(pil_list: list[Image.Image]) -> list[list[Image.Image]]:
        """图片列表编组."""
        new_list = []

        in_list = []
        ver_ratio = 2
        her_ratio = 0.8
        ver_image_len = 2
        her_image_len = 3
        for num, obj in enumerate(pil_list):
            in_list.append(obj)

            if (
                obj.width / obj.height > ver_ratio
                or (
                    obj.width / obj.height > her_ratio and len(in_list) >= ver_image_len
                )
                or len(in_list) >= her_image_len
                or num + 1 == len(pil_list)
            ):
                new_list.append(in_list.copy())
                in_list = []

        return new_list

    def fun_制作单排图片(self, pil_list: list[Image.Image]) -> Image.Image:
        """制作单排图片."""
        ori_width = self.width - ((len(pil_list) + 1) * self.gutter)
        all_ratio = sum([obj.width / obj.height for obj in pil_list])
        col_width = ori_width / all_ratio
        small_height = int(ori_width / all_ratio)

        pil_list = [
            self.fun_制作单个图片(obj, col_width, small_height) for obj in pil_list
        ]

        return fun_图片横向拼接(
            pil_list,
            self.gutter,
            "center",
            (255, 255, 255, 255),
        )

    def fun_制作单个图片(
        self,
        obj: Image.Image,
        col_width: float,
        small_height: int,
    ) -> Image.Image:
        """制作单个图片."""
        small_width = int(col_width * (obj.width / obj.height))
        obj = fun_图片裁剪(obj, small_width, small_height, "center")
        obj = fun_图片画边框(obj, (240, 240, 240, 255))
        return fun_图片切换到圆角(obj, self.radio, (255, 255, 255, 255))

    def fun_制作日历图片(self, comb_pil_list: list[list[Image.Image]]) -> Image.Image:
        """制作日历图片."""
        pil = fun_图片竖向拼接(
            [self.fun_制作单排图片(obj) for obj in comb_pil_list],
            self.gutter,
            "center",
            (255, 255, 255, 255),
        )
        return fun_图片扩大粘贴(
            pil,
            self.width,
            pil.height + (self.gutter * 2),
            "center",
            "center",
            (255, 255, 255, 255),
        )

    def main(self) -> None:
        """制作日历图片."""
        for in_path in tqdm(
            list(self.material_path.iterdir()),
            ncols=100,
            desc="制作日历图片\t",
        ):
            png_path = in_path.parent / (in_path.name + ".png")
            if in_path.is_dir() and png_path.exists() is False:
                png_list = self.fun_获取文件夹所有图片(in_path)
                png_list = self.fun_图片列表编组(png_list)  # type: ignore
                pil = self.fun_制作日历图片(png_list)

                pil.save(png_path.as_posix())
