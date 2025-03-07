import math
from functools import cached_property

from PIL import Image

from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.fun_图片编辑 import fun_图片横向拼接, fun_图片裁剪


class Layout1大3小自适应(LayoutInit):
    @cached_property
    def fun_first_image(self):
        im = self._pil_list[0]
        im_height = math.ceil(self.xq_width / (im.width / im.height))
        im_height = max(im_height, self.xq_height - 250)
        # im = im.resize((self.xq_width, im_height), resample=Image.Resampling.LANCZOS)
        im = fun_图片裁剪(
            im=im,
            width=self.xq_width,
            height=im_height,
            position="center",
        )
        return im

    @cached_property
    def bottom_height(self) -> int:
        bottom_height = self.xq_height - self.fun_first_image.height - 50
        if bottom_height < 300:
            return 300
        return bottom_height

    def main(self):
        bottom_list = self._pil_list[1:4]
        small_width = math.ceil(
            (self.xq_width - ((len(bottom_list) - 1) * self.spacing))
            / len(bottom_list),
        )

        bottom_im_list = []
        for im in bottom_list:
            im = fun_图片裁剪(
                im=im,
                width=small_width,
                height=math.ceil(small_width / (im.width / im.height)),
                position="center",
            )
            bottom_im_list.append(im)

        bottom_im = fun_图片横向拼接(
            image_list=bottom_im_list,
            spacing=self.spacing,
            align_item="end",
            background_color=(255, 255, 255, 0),
        )

        bg = Image.new("RGBA", (self.xq_width, self.xq_height))
        bg.paste(self.fun_first_image, (0, 0), self.fun_first_image)
        bg.paste(bottom_im, (0, self.xq_height - bottom_im.height), bottom_im)

        return bg
