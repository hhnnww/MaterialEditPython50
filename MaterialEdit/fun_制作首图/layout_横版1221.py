import math
from functools import cached_property
from itertools import cycle

from PIL import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪


class Layout_横版1221(LayoutInit):
    @cached_property
    def fun_小图尺寸(self) -> tuple[int, int]:
        small_width = math.ceil((self.xq_width - (self.spacing * 2)) / 3)
        small_height = math.ceil((self.xq_height - (self.spacing * 3)) / 4)
        return (small_width, small_height)

    @cached_property
    def fun_大图尺寸(self) -> tuple[int, int]:
        width = (self.fun_小图尺寸[0] * 2) + self.spacing
        height = (self.fun_小图尺寸[1] * 2) + self.spacing
        return (width, height)

    def fun_横版1221(self) -> Image.Image:
        image_list = cycle(self.image_list)

        num = 1
        im_list = []
        for image in image_list:
            im = Image.open(image.path)
            im = im.convert("RGBA")
            if num in [1, 6]:
                im_list.append(
                    fun_图片裁剪(
                        im,
                        width=self.fun_大图尺寸[0],
                        height=self.fun_大图尺寸[1],
                        position=self.crop_position,
                    ),
                )
            else:
                im_list.append(
                    fun_图片裁剪(
                        im,
                        width=self.fun_小图尺寸[0],
                        height=self.fun_小图尺寸[1],
                        position=self.crop_position,
                    ),
                )

            num += 1

            if len(im_list) == 6:
                break

        for im in im_list:
            print(im.size)

        top_r = fun_图片竖向拼接(
            image_list=[im_list[1], im_list[2]],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        top = fun_图片横向拼接(
            image_list=[im_list[0], top_r],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bottom_l = fun_图片竖向拼接(
            image_list=[im_list[3], im_list[4]],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bottom = fun_图片横向拼接(
            image_list=[bottom_l, im_list[5]],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        bg = fun_图片竖向拼接(
            image_list=[top, bottom],
            spacing=self.spacing,
            align_item="center",
            background_color=self.bg_color,
        )

        return bg
