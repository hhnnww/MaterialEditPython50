from __future__ import annotations

from enum import Enum

from PIL import Image


class Align(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3


class ImageFuns:
    @staticmethod
    def fun_图片添加背景(
        im: Image.Image,
        bg_color: tuple[int, int, int, int] | tuple[int, int, int],
    ) -> Image.Image:
        """图片添加背景

        :param im: 图片对象
        :param bg_color: 背景颜色
        :return: 添加背景后的图片对象
        """
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        new_im = Image.new("RGBA", im.size, bg_color)
        new_im.paste(im, (0, 0), im)
        return new_im

    @staticmethod
    def fun_图片扩大(
        im: Image.Image,
        size: tuple[int, int],
        left_align: Align,
        right_align: Align,
    ) -> Image.Image:
        """图片扩大

        :param im: 图片对象
        :param size: 扩大后的大小
        :param left_align: 左对齐方式
        :param right_align: 右对齐方式
        :return: 扩大后的图片对象
        """
        # 获取原始图片的大小
        width, height = im.size

        # 计算新的大小
        new_width, new_height = size

        # 创建新的图片对象
        new_im = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))

        # 计算左上角的坐标
        if left_align == Align.LEFT:
            x = 0
        elif left_align == Align.CENTER:
            x = (new_width - width) // 2
        elif left_align == Align.RIGHT:
            x = new_width - width

        if right_align == Align.LEFT:
            y = 0
        elif right_align == Align.CENTER:
            y = (new_height - height) // 2
        elif right_align == Align.RIGHT:
            y = new_height - height

        # 将原始图片粘贴到新的图片上
        new_im.paste(im, (x, y), im)

        return new_im.convert("RGBA")


if __name__ == "__main__":
    # 测试代码
    img = Image.open(r"F:\饭桶设计\4000-4999\4266\4266\饭桶设计(8).jpg")
    enlarged_img = ImageFuns.fun_图片扩大(
        img,
        (img.width + 200, img.height + 200),
        Align.CENTER,
        Align.CENTER,
    )
    enlarged_img = ImageFuns.fun_图片添加背景(
        enlarged_img,
        (255, 255, 255, 255),
    )
    enlarged_img.show()
