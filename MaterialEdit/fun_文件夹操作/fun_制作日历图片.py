from pathlib import Path

from PIL import Image
from tqdm import tqdm

from ..fun_图片编辑 import ImageEdit
from .fun_遍历指定文件 import rglob


class MakeCalenderPic:
    def __init__(self, material_path: str):
        self.material_path = Path(material_path)
        self.gutter = 10
        self.width = 750
        self.radio = 10

    @staticmethod
    def fun_判断横竖版本(png_list: list[Image.Image]):
        average_ratio = sum([obj.width / obj.height for obj in png_list]) / len(
            png_list,
        )
        if average_ratio > 0.7:
            return "h"

        return "s"

    @staticmethod
    def fun_获取文件夹所有图片(sub_path: Path) -> list[Image.Image]:
        png_file_list = [
            Image.open(obj.as_posix()) for obj in rglob(folder=sub_path.as_posix(), suffix=[".png"])
        ]
        png_file_list.sort(key=lambda k: k.width / k.height, reverse=True)

        return png_file_list

    @staticmethod
    def fun_图片列表编组(pil_list: list[Image.Image]):
        new_list = []

        in_list = []
        for num, obj in enumerate(pil_list):
            in_list.append(obj)

            if (
                obj.width / obj.height > 2
                or (obj.width / obj.height > 0.8 and len(in_list) >= 2)
                or len(in_list) >= 3
                or num + 1 == len(pil_list)
            ):
                new_list.append(in_list.copy())
                in_list = []

        return new_list

    def fun_制作单排图片(self, pil_list: list[Image.Image]) -> Image.Image:
        ori_width = self.width - ((len(pil_list) + 1) * self.gutter)
        all_ratio = sum([obj.width / obj.height for obj in pil_list])
        col_width = ori_width / all_ratio
        small_height = int(ori_width / all_ratio)

        pil_list = [self.fun_制作单个图片(obj, col_width, small_height) for obj in pil_list]

        return ImageEdit.fun_图片横向拼接(
            pil_list,
            self.gutter,
            "center",
            (255, 255, 255, 255),
        )

    def fun_制作单个图片(self, obj: Image.Image, col_width: float, small_height: int):
        small_width = int(col_width * (obj.width / obj.height))
        obj = ImageEdit.fun_图片裁剪(obj, small_width, small_height, "center")
        obj = ImageEdit.fun_图片画边框(obj, (240, 240, 240, 255))
        obj = ImageEdit.fun_图片切换到圆角(obj, self.radio, (255, 255, 255, 255))
        return obj

    def fun_制作日历图片(self, comb_pil_list: list[list[Image.Image]]) -> Image.Image:
        pil = ImageEdit.fun_图片竖向拼接(
            [self.fun_制作单排图片(obj) for obj in comb_pil_list],
            self.gutter,
            "center",
            (255, 255, 255, 255),
        )
        pil = ImageEdit.fun_图片扩大粘贴(
            pil,
            self.width,
            pil.height + (self.gutter * 2),
            "center",
            "center",
            (255, 255, 255, 255),
        )
        return pil

    def main(self):
        for in_path in tqdm(
            list(self.material_path.iterdir()),
            ncols=100,
            desc="制作日历图片\t",
        ):
            png_path = in_path.parent / (in_path.name + ".png")
            if in_path.is_dir() and png_path.exists() is False:
                png_list = self.fun_获取文件夹所有图片(in_path)
                png_list = self.fun_图片列表编组(png_list)
                pil = self.fun_制作日历图片(png_list)

                pil.save(png_path.as_posix())
