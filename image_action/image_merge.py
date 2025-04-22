"""图像合并类。

此类用于将多个图像按照指定方向、间距和对齐方式合并为一个图像。
类:
    ImageMerge:
        初始化方法:
                    "x" 表示水平合并，"y" 表示垂直合并。
                align (Literal["start", "center", "end"]): 图像对齐方式。
        方法:
            main() -> Image.Image:
                主函数，用于将多个图像合并为一个图像。
                返回:
                异常:
                    - 支持通过 `align` 参数设置对齐方式，
                    "start"（起始对齐）
                    "center"（居中对齐）
                    "end"（末端对齐）。
                    - `align` 可选值为 "start"、"center" 或 "end"。
"""

from typing import Literal

from PIL import Image


class ImageMerge:
    @staticmethod
    def fun_图片横向拼接(
        image_list: list[Image.Image],
        spacing: int,
        align: Literal["start", "center", "end"],
    ) -> Image.Image:
        """图片横向拼接函数。"""
        widths, heights = zip(*(img.size for img in image_list))
        # 计算总宽度和最大高度
        total_width = sum(widths) + spacing * (len(image_list) - 1)
        max_height = max(heights)
        merged_image = Image.new("RGBA", (total_width, max_height), (255, 255, 255, 0))

        # 根据对齐方式计算偏移量
        offset = 0
        for img in image_list:
            y_offset = 0
            if align == "center":
                y_offset = (max_height - img.height) // 2
            elif align == "end":
                y_offset = max_height - img.height
            merged_image.paste(img, (offset, y_offset), img)
            offset += img.width + spacing
        return merged_image

    @staticmethod
    def fun_图片竖向拼接(
        image_list: list[Image.Image],
        spacing: int,
        align: Literal["start", "center", "end"],
    ) -> Image.Image:
        """图片竖向拼接函数。"""
        # 计算总高度和最大宽度
        widths, heights = zip(*(img.size for img in image_list))
        total_height = sum(heights) + (spacing * (len(image_list) - 1))
        max_width = max(widths)
        merged_image = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))

        # 根据对齐方式计算偏移量
        offset = 0
        for img in image_list:
            x_offset = 0
            if align == "center":
                x_offset = int((max_width - img.width) / 2)
            elif align == "end":
                x_offset = max_width - img.width
            merged_image.paste(img, (x_offset, offset), img)
            offset += img.height + spacing
        return merged_image
