from PIL.Image import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit


class Layout13_2(LayoutInit):
    @property
    def small_width(self) -> int:
        """计算小图宽度."""
        if self.radio:
            return (self.xq_width - (self.spacing * 4)) // 3

        return (self.xq_width - (self.spacing * 2)) // 3

    @property
    def small_height(self) -> int:
        """计算小图高度."""
        if self.radio:
            return (self.xq_height - (self.spacing * 5)) // 4

        return (self.xq_height - (self.spacing * 3)) // 4

    @property
    def large_size(self) -> tuple[int, int]:
        """计算大图尺寸."""
        width = (self.small_width * 3) + (self.spacing * 2)
        height = (self.small_height * 3) + (self.spacing * 2)
        return width, height

    def main(self) -> Image:
        large_im = ImageAction.fun_图片添加圆角(
            ImageAction.fun_图片裁剪(
                self._pil_list[0],
                self.large_size,
                "center",
            ),
            self.image_radio,
        )

        bottom_im = ImageAction.fun_图片横向拼接(
            image_list=[
                ImageAction.fun_图片添加圆角(
                    ImageAction.fun_图片裁剪(
                        pil,
                        (self.small_width, self.small_height),
                        "center",
                    ),
                    self.image_radio,
                )
                for pil in self._pil_list[1:4]
            ],
            spacing=self.spacing,
            align="start",
        )

        bg = ImageAction.fun_图片竖向拼接(
            image_list=[large_im, bottom_im],
            spacing=self.spacing,
            align="start",
        )

        return ImageAction.fun_图片添加背景(
            ImageAction.fun_图片扩大(
                bg,
                (self.xq_width, self.xq_height),
                Align.CENTER,
                Align.CENTER,
            ),
            self.bg_color,
        )
