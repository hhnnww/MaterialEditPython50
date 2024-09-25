import shutil
from pathlib import Path

import pythoncom
import pywintypes
from PIL import Image
from win32com.client import DispatchEx

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件
from MaterialEdit.setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO


class PPT导出图片:
    def __init__(self, ppt_path: Path, effect_path: str) -> None:
        self.ppt_path = ppt_path
        self.ppt_dir = ppt_path.parent / ppt_path.stem
        self.png_path = ppt_path.with_suffix(".png")

        self.spacing = 10

        self.line_col = 3
        self.line = 4

        self.effect_path = Path(effect_path)
        if self.effect_path.exists() is not True:
            self.effect_path.mkdir()

    @property
    def first_width(self):
        return self.pic_width - self.spacing * 2

    @property
    def small_width(self):
        return int(
            (self.pic_width - ((self.line_col + 1) * self.spacing)) / self.line_col
        )

    @property
    def pic_width(self) -> int:
        im = Image.open(self.pic_files[0])
        return im.width

    @property
    def pic_files(self):
        pic_files = fun_遍历指定文件(
            folder=self.ppt_dir.as_posix(), suffix=[".png", ".jpeg", ".jpg"]
        )
        if len(pic_files) < 13:
            pic_files += pic_files

        return pic_files

    def fun_ppt导出图片(self):
        pythoncom.CoInitialize()  # type: ignore
        ppt_app = DispatchEx("PowerPoint.Application")
        ppt_app.DisplayAlerts = 0

        try:
            ppt = ppt_app.Presentations.Open(self.ppt_path.as_posix())
        except pywintypes.com_error:  # type: ignore
            return

        try:
            ppt.SaveAs(self.ppt_dir, 17)
        except pywintypes.com_error:  # type: ignore
            ppt.Close()
            return

        if self.ppt_path.suffix.lower() == ".ppt":
            ppt.SaveAs(self.ppt_path.with_suffix(".pptx"))
            self.ppt_path.unlink()

        ppt.Save()
        ppt.Close()

    def fun_图片合并(self):
        if self.ppt_dir.exists() is not True:
            return

        bottom_list = []
        bg_list = []
        in_line_list = []
        for num, pic in enumerate(self.pic_files):
            im = Image.open(pic)
            im = im.convert("RGBA")

            if num == 0:
                im.thumbnail(
                    (self.first_width, 9999), resample=Image.Resampling.LANCZOS
                )

                if self.spacing > 0:
                    im = fun_图片画边框(im=im, border_color=FIRST_IMAGE_BORDER_COLOR)
                    im = fun_图片切换到圆角(im=im, border_radius=FIRST_IMAGE_RATIO)

                bg_list.append(im.copy())

            else:
                im.thumbnail(
                    (self.small_width, 9999), resample=Image.Resampling.LANCZOS
                )

                if self.spacing > 0:
                    im = fun_图片画边框(im=im, border_color=FIRST_IMAGE_BORDER_COLOR)
                    im = fun_图片切换到圆角(im=im, border_radius=FIRST_IMAGE_RATIO)

                in_line_list.append(im.copy())

            if len(in_line_list) == self.line_col:
                line_im = fun_图片横向拼接(
                    image_list=in_line_list,
                    spacing=self.spacing,
                    align_item="start",
                    background_color=(255, 255, 255, 255),
                )
                bottom_list.append(line_im.copy())
                in_line_list = []

            if len(bottom_list) == self.line:
                break

        bottom_im = fun_图片竖向拼接(
            image_list=bottom_list,
            spacing=self.spacing,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        bg_list.append(bottom_im)

        bg = fun_图片竖向拼接(
            image_list=bg_list,
            spacing=self.spacing,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        bg = fun_图片扩大粘贴(
            im=bg,
            width=bg.width + 20,
            height=bg.height + 20,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )

        bg.save(self.png_path.as_posix())
        bg.save(self.effect_path / self.png_path.name)
        shutil.rmtree(self.ppt_dir)

    def fun_备份首图(self):
        if self.ppt_dir.exists() is not True:
            return

        for in_file in self.ppt_dir.iterdir():
            if in_file.is_file() and "1" in in_file.stem:
                effect_image_path = self.effect_path / f"{self.ppt_path.stem}.jpg"
                shutil.copy(in_file, effect_image_path)
                break

    def main(self):
        self.fun_ppt导出图片()
        # self.fun_备份首图()
        self.fun_图片合并()
