"""image add radius"""

from PIL import Image

from image_action.image_shape import ImageShape


class ImageAddRadius:
    @staticmethod
    def fun_图片添加圆角(im: Image.Image, radius: int) -> Image.Image:
        """为给定的图像添加圆角效果。

        参数:
            im (Image.Image): 要处理的Pillow图像对象。
            radius (int): 圆角的半径大小。
        返回:
            Image.Image: 添加圆角效果后的图像对象。
        """
        bg = ImageShape.fun_画一个圆角矩形(
            im.size,
            radius,
            (255, 255, 255, 255),
        )
        with im:
            bg.paste(im, (0, 0), bg)

        return bg


if __name__ == "__main__":
    im = Image.open(r"F:\小夕素材\11000-11999\11243\11243\小夕素材(73).png")
    ImageAddRadius.fun_图片添加圆角(im=im, radius=60).show()
