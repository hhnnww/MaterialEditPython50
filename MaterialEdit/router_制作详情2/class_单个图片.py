import math
from functools import cached_property
from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import (
    fun_单行文字转图片,
)
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片2 import (
    fun_单行文字转图片2,
)
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class ClassOneImage:
    def __init__(
        self,
        image_pil: Image.Image,
        image_path: Path,
        image_width: int,
        background_color: tuple[int, int, int, int],
        shop_name: str,
        has_name: bool,
        all_material_file: list[Path],
        has_water: bool,
    ) -> None:
        self.image_pil = image_pil
        self.image_width = image_width
        self.background_color = background_color
        self.shop_name = shop_name
        self.has_name = has_name
        self.image_path = image_path
        self.all_material_file = all_material_file
        self.has_water = has_water

    text_color = (120, 120, 120, 255)
    logo_to_text_space = 30

    @cached_property
    def fun_获取对应源文件(self) -> Path:
        for in_file in self.all_material_file:
            if in_file.stem in self.image_path.stem and self.shop_name in in_file.stem:
                return in_file

        return self.image_path

    @cached_property
    def fun_图片比例(self):
        return self.image_pil.width / self.image_pil.height

    @cached_property
    def __fun_图片中间广告图片(self) -> Image.Image:
        ad_pil = fun_单行文字转图片(
            text=f"淘宝:{self.shop_name}",
            background_color=(0, 0, 0, 0),
            chinese_font_name="zihun",
            english_font_name="lato",
            font_weight="normal",
            font_size=40,
            fill_color=(120, 120, 120, 30),
        )

        if ad_pil.width > self.image_width / 4:
            ad_pil.thumbnail((int(self.image_width / 4), 999999))

        return ad_pil

    @cached_property
    def __fun_原始图片(self) -> Image.Image:
        im = self.image_pil
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")
        return im

    @property
    def __fun_图片名称(self) -> Image.Image:
        return fun_单行文字转图片2(
            text=self.fun_获取对应源文件.name.upper(),
            size=50,
            fill=self.text_color,
            background=self.background_color,
            font_weight="light",
        )

    @property
    def __fun_图片尺寸(self) -> Image.Image:
        if self.fun_获取对应源文件.suffix.lower() in [".psd", ".psb", ".jpg", ".png"]:
            text = f"{self.__fun_原始图片.width}×{self.__fun_原始图片.height} (px)"
        else:
            text = " "

        return fun_单行文字转图片2(
            text=text,
            size=35,
            fill=self.text_color,
            background=self.background_color,
            font_weight="light",
        )

    @cached_property
    def __fun_制作小图(self) -> Image.Image:
        ori_im = self.__fun_原始图片
        height = math.ceil(self.image_width / (ori_im.width / ori_im.height))
        max_height = 5000

        if height > max_height:
            small_im = fun_图片裁剪(
                im=ori_im, width=self.image_width, height=max_height, position="start"
            )

        else:
            small_im = ori_im.resize(
                (self.image_width, height),
                resample=Image.Resampling.LANCZOS,
                reducing_gap=8,
            )

        if self.has_water is True:
            for left in [
                30,
                int((small_im.width - self.__fun_图片中间广告图片.width) / 2),
                small_im.width - self.__fun_图片中间广告图片.width - 30,
            ]:
                for top in [
                    30,
                    int((small_im.height - self.__fun_图片中间广告图片.height) / 2),
                    small_im.height - self.__fun_图片中间广告图片.height - 30,
                ]:
                    r, g, b, a = self.__fun_图片中间广告图片.split()
                    small_im.paste(
                        self.__fun_图片中间广告图片,
                        (
                            left,
                            top,
                        ),
                        a,
                    )

        return small_im

    def main(self):
        if self.has_name:
            bottom_im = fun_图片竖向拼接(
                image_list=[
                    self.__fun_图片名称,
                    self.__fun_图片尺寸,
                ],
                spacing=25,
                align_item="center",
                background_color=self.background_color,
            )

            bottom_im = fun_图片竖向拼接(
                image_list=[
                    fun_获取单个水印(size=60, fill_clor=self.text_color),
                    bottom_im,
                ],
                spacing=self.logo_to_text_space,
                align_item="center",
                background_color=self.background_color,
            )

            bottom_im.thumbnail(
                (math.ceil(self.image_width * 0.7), 999999),
                resample=Image.Resampling.LANCZOS,
                reducing_gap=8,
            )

            bottom_im = fun_图片扩大粘贴(
                im=bottom_im,
                width=self.image_width,
                height=bottom_im.height + 180,
                left="center",
                top="start",
                background_color=self.background_color,
            )

            return fun_图片竖向拼接(
                image_list=[self.__fun_制作小图, bottom_im],
                spacing=50,
                align_item="center",
                background_color=self.background_color,
            )

        return self.__fun_制作小图
