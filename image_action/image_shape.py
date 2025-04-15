"""该模块提供了一个 `ImageShape` 类，用于创建各种形状的图像。"""

from PIL import Image, ImageDraw


class ImageShape:
    @staticmethod
    def fun_画一个圆(
        size: int,
        fill_color: tuple[int, int, int, int],
    ) -> Image.Image:
        """创建一个指定大小和填充颜色的圆形图像。

        参数:
            size (int): 圆形的目标大小（宽和高相等）。
            fill_color (tuple[int, int, int, int]):
                圆形的填充颜色，格式为 (R, G, B, A)。
        返回:
            Image.Image: 包含圆形的Pillow图像对象。
        """
        zoom = 10
        image = Image.new("RGBA", (size * 5, size * 5), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size * zoom, size * zoom), fill=fill_color)
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        return image

    @staticmethod
    def fun_画一个矩形(
        size: tuple[int, int],
        fill_color: tuple[int, int, int, int],
    ) -> Image.Image:
        """创建一个指定大小和填充颜色的矩形图像。

        参数:
            size (tuple[int, int]): 矩形的宽和高。
            fill_color (tuple[int, int, int, int]):
            矩形的填充颜色，格式为 (R, G, B, A)。
        返回:
            Image.Image: 包含矩形的Pillow图像对象。
        """
        return Image.new("RGBA", size, fill_color)

    @staticmethod
    def fun_画一个圆角矩形(
        size: tuple[int, int],
        radiu: int,
        fill_color: tuple[int, int, int, int],
    ) -> Image.Image:
        """创建一个指定大小、圆角半径和填充颜色的圆角矩形图像。

        参数:
            size (tuple[int, int]): 圆角矩形的宽和高。
            radiu (int): 圆角的半径。
            fill_color (tuple[int, int, int, int]):
                圆角矩形的填充颜色，格式为 (R, G, B, A)。
        返回:
            Image.Image: 包含圆角矩形的Pillow图像对象。
        """
        zoom = 10
        width = size[0] * zoom
        height = size[1] * zoom
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 绘制圆角矩形
        draw.rounded_rectangle(
            (0, 0, width, height),
            radius=radiu * zoom,
            fill=fill_color,
        )
        image.thumbnail(size, Image.Resampling.LANCZOS)
        return image

    @staticmethod
    def fun_画一个纯圆角矩形(
        size: tuple[int, int],
        fill_color: tuple[int, int, int, int],
    ) -> Image.Image:
        """创建一个指定大小和填充颜色的纯圆角矩形图像。

        参数:
            size (tuple[int, int]): 圆角矩形的宽和高。
            fill_color (tuple[int, int, int, int]):
            圆角矩形的填充颜色，格式为 (R, G, B, A)。
        返回:
            Image.Image: 包含纯圆角矩形的Pillow图像对象。
        """
        zoom = 10
        width = size[0] * zoom
        height = size[1] * zoom
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 绘制纯圆角矩形
        draw.rounded_rectangle(
            (0, 0, width, height),
            radius=min(size) * zoom // 2,
            fill=fill_color,
        )
        image.thumbnail(size, Image.Resampling.LANCZOS)
        return image


if __name__ == "__main__":
    ImageShape.fun_画一个纯圆角矩形((800, 200), (255, 255, 255, 255)).show()
