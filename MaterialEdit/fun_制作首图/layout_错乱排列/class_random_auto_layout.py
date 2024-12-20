"""错乱排列."""

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框


class RandomAutoLayout:
    """首图错乱排列."""

    def __init__(
        self,
        image_list: list[str],
        line_row: int,
        width: int,
        height: int,
    ) -> None:
        """错乱排列."""
        self.image_list = image_list
        self.line_row = line_row

        self.width = width
        self.height = height
        self.gutter = 10

    def _fun_构建列表(self) -> list[Image.Image]:
        pil_list = []
        for in_file in self.image_list:
            im = Image.open(in_file)
            im = self._fun_构建小图片(im=im)
            pil_list.append(im)
        return pil_list

    @property
    def small_height(self) -> int:
        """小图高度."""
        return int((self.height - ((self.line_row + 1) * self.gutter)) / self.line_row)

    def main(self):
        row_list = []
        for in_line_list in self._fun_构建组合列表():
            row_list.append(self._fun_制作单行图片(inline_list=in_line_list))

        bg = fun_图片竖向拼接(
            image_list=row_list,
            spacing=self.gutter,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        return fun_图片扩大粘贴(
            im=bg,
            width=self.width,
            height=self.height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )

    def _fun_制作单行图片(self, inline_list: list[Image.Image]) -> Image.Image:
        im = fun_图片横向拼接(
            image_list=inline_list,
            spacing=self.gutter,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )
        left = int((im.width - self.width) / 2)
        return im.crop((left, 0, left + self.width, im.height))

    def _fun_构建组合列表(self) -> list[list[Image.Image]]:
        comb_image_list = []

        in_line_list = []
        in_line_width = 0
        for in_im in self._fun_构建列表():
            in_line_list.append(in_im)
            in_line_width += in_im.width + self.gutter

            if in_line_width > self.width:
                comb_image_list.append(in_line_list.copy())
                in_line_list = []
                in_line_width = 0

            if len(comb_image_list) == self.line_row:
                break

        return comb_image_list

    def _fun_构建小图片(self, im: Image.Image) -> Image.Image:
        im_ratio = im.width / im.height
        im_width = int(self.small_height * im_ratio)
        im = im.resize(size=(im_width, self.small_height), resample=Image.Resampling.LANCZOS)
        im = fun_图片画边框(im=im, border_color=(240, 240, 240, 250), width=1)
        im = fun_图片切换到圆角(
            im=im,
            border_radius=8,
            background_color=(255, 255, 255, 255),
        )
        return im
