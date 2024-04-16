import re
from pathlib import Path
from typing import List, Literal

from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class LayoutRandomLayoug:
    def __init__(
        self,
        image_list: List[str],
        layout_str: str,
        width: int,
        height: int,
        crop_position: Literal["start", "center", "end"],
    ) -> None:
        """
        :param List[str] image_list: 图片列表
        :param str layout_str: 布局本文 4-5-shadow这样的
        :param int width: 大图宽度
        :param int height: 大图高度
        :param Literal[start, center, end] crop_position: 图片裁剪模式
        """
        self.image_list = image_list
        self.width = width
        self.height = height
        self.crop_position = crop_position
        self.line_col = int(self._fun_构建布局(layout=layout_str)[0])
        self.line_row = int(self._fun_构建布局(layout=layout_str)[1])

        self.gutter = 10
        self.shadow = False
        if "shadow" in layout_str:
            self.shadow = True
            # self.gutter = 0

        self.small_width = int(
            (self.width - ((self.line_col + 1) * self.gutter)) / self.line_col
        )
        self.small_height = int(
            (self.height - ((self.line_row + 1) * self.gutter)) / self.line_row
        )

    @staticmethod
    def _fun_构建布局(layout: str) -> List[str]:
        return re.findall("\d", layout)

    def _fun_阴影图片(self) -> Image.Image:
        """
        获取阴影图片路径
        然后打开并返回

        :return Image.Image: _description_
        """
        shadow_path = (
            Path(__file__).parent / f"{self.line_col}-{self.line_row}-item.png"
        )
        im = Image.open(shadow_path.as_posix())
        return im

    def _fun_构建图片列表(self):
        """
        图片如果长度不够 则自动增加
        """
        while len(self.image_list) < (self.line_col + 1) * self.line_row:
            self.image_list += self.image_list
        self.image_list = self.image_list[: (self.line_col + 1) * self.line_row]

    def _fun_构建PIL列表(self) -> List[List[Image.Image]]:
        self._fun_构建图片列表()

        pil_list = []
        inline_list = []
        for in_file in tqdm(self.image_list, ncols=100, desc=f"制作首图"):
            im = Image.open(in_file).convert("RGBA")
            im = fun_图片裁剪(
                im=im,
                width=self.small_width,
                height=self.small_height,
                position=self.crop_position,
            )

            # 如果没有阴影，则添加边框和圆角
            if self.shadow is False and self.gutter > 0:
                im = fun_图片画边框(im=im, border_color=(230, 230, 250, 255))
                im = fun_图片切换到圆角(
                    im=im, border_radius=8, background_color=(255, 255, 255, 255)
                )

            inline_list.append(im)

            if len(inline_list) == self.line_col + 1:
                pil_list.append(inline_list.copy())
                inline_list = []

            if len(pil_list) == self.line_row:
                break

        return pil_list

    def _fun_增加阴影(self, im: Image.Image):
        shadow_im = self._fun_阴影图片()

        if self.line_row == 3:
            left_dis = 24
            top_dis = 22
        elif self.line_row == 2:
            left_dis = 40 - self.gutter
            top_dis = 17

        left = int(self.small_width / 2) - left_dis - int(self.gutter / 2)
        top = top_dis
        num = 0
        while True:
            im.paste(shadow_im, (left, top), shadow_im)
            left += int(self.small_width * 2) + int(self.gutter * 2)

            if left >= im.width:
                top += self.small_height + self.gutter
                if num % 2 == 0:
                    left = (
                        int(self.small_width / 2)
                        - left_dis
                        - self.small_width
                        - int(self.gutter * 1.5)
                    )
                else:
                    left = int(self.small_width / 2) - left_dis - int(self.gutter / 2)

                num += 1

            if top >= im.height:
                break

        return im

    def main(self) -> Image.Image:
        pil_list = []
        for num, line_list in enumerate(self._fun_构建PIL列表()):
            line_im = fun_图片横向拼接(
                image_list=line_list,
                spacing=self.gutter,
                align_item="center",
                background_color=(255, 255, 255, 255),
            )

            # if self.line_row > 3:
            #     left = 0 - (self.gutter + 2)
            #     if num % 2 == 0:
            #         left = int((line_im.width - self.width) / 2)
            #     line_im = line_im.crop((left, 0, left + self.width, line_im.height))
            # else:
            #     left = int((line_im.width - self.width) / 2)
            #     line_im = line_im.crop((left, 0, left + self.width, line_im.height))

            left = int((line_im.width - self.width) / 2)
            line_im = line_im.crop((left, 0, left + self.width, line_im.height))

            pil_list.append(line_im)

        bg = fun_图片竖向拼接(
            image_list=pil_list,
            spacing=self.gutter,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片扩大粘贴(
            im=bg,
            width=self.width,
            height=self.height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )

        if self.shadow is True:
            bg = self._fun_增加阴影(im=bg)

        return bg
