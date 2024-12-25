"""PPT导出PNG图片"""

import contextlib
import shutil
from pathlib import Path

import pythoncom
import pywintypes
from PIL import Image
from win32com.client import DispatchEx

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


class PPT导出图片:
    """PPT导出PNG图片"""

    def __init__(
        self,
        ppt_path: Path,
    ) -> None:
        """PPT导出图片."""
        self.ppt_path = ppt_path
        self.ppt_dir = ppt_path.parent / ppt_path.stem
        self.png_path = ppt_path.with_suffix(".png")

        self.spacing = 5

        self.line_col = 3
        self.line = 4

    @property
    def first_width(self) -> int:
        """大图宽度"""
        return self.pic_width - self.spacing * 2

    @property
    def small_width(self) -> int:
        """小图宽度"""
        return int((self.pic_width - ((self.line_col + 1) * self.spacing)) / self.line_col)

    @property
    def pic_width(self) -> int:
        """获取图片原始宽度"""
        im = Image.open(self.pic_files[0])
        return im.width

    @property
    def pic_files(self) -> list[Path]:
        """获取所欲图片列表"""
        pic_files = rglob(
            folder=self.ppt_dir.as_posix(),
            suffix=[".png", ".jpeg", ".jpg"],
        )
        max_image_num = 13
        if len(pic_files) < max_image_num:
            pic_files += pic_files

        return pic_files

    def fun_ppt导出图片(self) -> None:
        """使用win32com导出所有图片"""
        pythoncom.CoInitialize()
        ppt_app = DispatchEx("PowerPoint.Application")
        ppt_app.DisplayAlerts = 0

        with contextlib.suppress(pywintypes.com_error):
            ppt = ppt_app.Presentations.Open(self.ppt_path.as_posix())
            ppt.SaveAs(self.ppt_dir, 17)
            if self.ppt_path.suffix.lower() == ".ppt":
                ppt.SaveAs(self.ppt_path.with_suffix(".pptx"))
                self.ppt_path.unlink()
            self.fun_图片合并()
            ppt.Close()

    def fun_图片合并(self) -> None:
        """合并所有小图片"""
        if self.ppt_dir.exists() is not True:
            return

        bottom_list = []
        bg_list = []
        in_line_list = []
        for num, pic in enumerate(self.pic_files):
            im = Image.open(pic)
            im = im.convert("RGBA")

            if num == 0:
                im.thumbnail((self.first_width, 9999), resample=Image.Resampling.LANCZOS)
                bg_list.append(im.copy())
            else:
                im.thumbnail((self.small_width, 9999), resample=Image.Resampling.LANCZOS)
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

        bg.save(self.png_path.as_posix())

    def main(self) -> None:
        """开始操作"""
        self.fun_ppt导出图片()

        if self.ppt_dir.exists() is True:
            shutil.rmtree(self.ppt_dir)
