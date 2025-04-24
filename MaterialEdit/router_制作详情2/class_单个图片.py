"""单个图片生成图像"""

import math
from functools import cached_property
from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_删除图片透明边框 import fun_删除图片透明边框
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_预览图水印.fun_单个预览图效果图水印 import (
    fun_单个预览图效果图水印,
)
from MaterialEdit.setting import FONT_COLOR


class ClassOneImage:
    """详情图中的单个图片处理"""

    def __init__(
        self,
        image_pil: Image.Image,
        image_path: Path,
        image_width: int,
        background_color: tuple[int, int, int, int],
        shop_name: str,
        all_material_file: list[Path],
        has_water: bool,
        has_name: bool,
        effect_has_watermark: bool,
    ) -> None:
        """处理单个图片."""
        self.image_pil = fun_删除图片透明边框(image_pil)
        self.image_width = image_width
        self.background_color = background_color
        self.shop_name = shop_name
        self.has_name = has_name
        self.image_path = image_path
        self.all_material_file = all_material_file
        self.has_water = has_water
        self.effect_has_watermark = effect_has_watermark

    text_color = FONT_COLOR
    logo_to_text_space = 30

    @cached_property
    def fun_获取对应源文件(self) -> Path:
        """根据图片路径获取源文件路径"""
        for in_file in self.all_material_file:
            if in_file.stem in self.image_path.stem and self.shop_name in in_file.stem:
                return in_file

        return self.image_path

    @cached_property
    def fun_图片比例(self) -> float:
        """计算图片比例"""
        return self.image_pil.width / self.image_pil.height

    @cached_property
    def __fun_原始图片(self) -> Image.Image:
        im = self.image_pil
        if im.mode.lower() != "rgba":
            im = im.convert(mode="RGBA")
        return im

    @property
    def __fun_图片名称(self) -> Image.Image:
        return MakeIbmFont(
            text=self.fun_获取对应源文件.name.upper(),
            size=50,
            color=self.text_color,
            bg_color=self.background_color,
            weight="light",
        ).main()

    @property
    def __fun_图片尺寸(self) -> Image.Image:
        text = " "
        if self.fun_获取对应源文件.suffix.lower() in [".psd", ".psb", ".jpg", ".png"]:
            text = f"{self.__fun_原始图片.width}×{self.__fun_原始图片.height} (px)"
        elif self.fun_获取对应源文件.suffix.lower() in [".ai", ".eps"]:
            text = "AI矢量设计素材"
        elif self.fun_获取对应源文件.suffix.lower() in [".pptx", ".ppt"]:
            text = "PPT幻灯片素材"

        return MakeIbmFont(
            text=text.upper(),
            size=40,
            color=self.text_color,
            bg_color=self.background_color,
            weight="light",
        ).main()

    @cached_property
    def __fun_制作小图(self) -> Image.Image:
        ori_im = self.__fun_原始图片
        height = math.ceil(self.image_width / (ori_im.width / ori_im.height))

        return ori_im.resize(
            size=(self.image_width, height),
            resample=Image.Resampling.LANCZOS,
            reducing_gap=8,
        )

    def __str__(self) -> str:
        """打印名."""
        return self.image_path.name

    def main(self) -> Image.Image:
        """生成详情中的单个图片

        Returns:
            Image.Image: _description_

        """
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
                    fun_获取单个水印(size=120, fill_clor=self.text_color),
                    bottom_im,
                ],
                spacing=self.logo_to_text_space,
                align_item="center",
                background_color=self.background_color,
            )

            bottom_im.thumbnail(
                size=(math.ceil(self.image_width * 0.7), 999999),
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

        if self.effect_has_watermark is True:
            logo = fun_单个预览图效果图水印(shop_name=self.shop_name, cate="xgt")
            logo.thumbnail((200, 200), Image.Resampling.LANCZOS)
            small_im = self.__fun_制作小图
            small_im.paste(logo, (50, small_im.height - logo.height - 50), logo)
            return small_im

        return self.__fun_制作小图
