"""裁剪图像到指定大小并根据对齐方式进行裁剪。"""

from typing import Literal

from PIL import Image


class ImageCrop:
    @staticmethod
    def fun_图片裁剪(
        im: Image.Image,
        size: tuple[int, int],
        align: Literal["start", "center", "end"],
    ) -> Image.Image:
        """裁剪图像到指定大小并根据对齐方式进行裁剪。

        参数:
            im (Image.Image): 输入的Pillow图像对象。
            size (tuple[int, int]): 目标图像的宽度和高度 (宽, 高)。
            align (Literal["start", "center", "end"]): 裁剪对齐方式。
                - "start": 从左上角对齐裁剪。
                - "center": 从中心对齐裁剪。
                - "end": 从右下角对齐裁剪。
        返回:
            Image.Image: 裁剪后的Pillow图像对象。
        """
        # Calculate the target aspect ratio
        target_aspect = size[0] / size[1]
        original_aspect = im.width / im.height

        # Resize the image while maintaining aspect ratio
        if original_aspect > target_aspect:
            # Wider image, fit height and scale width
            new_height = size[1]
            new_width = int(size[1] * original_aspect)
        else:
            # Taller image, fit width and scale height
            new_width = size[0]
            new_height = int(size[0] / original_aspect)

        im_resized = im.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Calculate cropping box based on alignment
        if align == "start":
            left = 0
            top = 0
        elif align == "center":
            left = (new_width - size[0]) // 2
            top = (new_height - size[1]) // 2
        elif align == "end":
            left = new_width - size[0]
            top = new_height - size[1]

        right = left + size[0]
        bottom = top + size[1]

        # Crop the image to the desired size
        return im_resized.crop((left, top, right, bottom))
