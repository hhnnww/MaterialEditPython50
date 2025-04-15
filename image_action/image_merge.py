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

from pathlib import Path
from typing import Literal

from PIL import Image


class ImageMerge:
    def __init__(
        self,
        image_list: list[Image.Image],
        direction: Literal["x", "y"],
        spacing: int,
        align: Literal["start", "center", "end"],
    ) -> None:
        """初始化方法。

        参数:
            image_list (list[Image.Image]): 图像对象的列表。
            direction (Literal["x", "y"]): 合并图像的方向。
            spacing (int): 图像之间的间距（以像素为单位）。
            align (Literal["start", "center", "end"]): 图像对齐方式，
                "start" 表示起始对齐，"center" 表示居中对齐，"end" 表示末尾对齐。
        """
        self.image_list = image_list
        self.direction = direction
        self.spacing = spacing
        self.align = align

    def main(self) -> Image.Image:
        """主函数，用于将多个图像合并为一个图像。

        Returns:
            Image.Image: 合并后的图像对象。
        Raises:
            ValueError: 如果图像列表为空或方向无效时抛出。
        功能描述:
            - 如果 `direction` 为 "x"，图像将水平合并。
            - 如果 `direction` 为 "y"，图像将垂直合并。
            - 支持通过 `align` 参数设置对齐方式，
                包括 "center"（居中对齐）和 "end"（末端对齐）。
            - 支持通过 `spacing` 参数设置图像之间的间距。
        注意:
            - `image_list` 是一个包含 PIL 图像对象的列表。
            - `direction` 必须是 "x" 或 "y"。
            - `align` 可选值为 "center" 或 "end"。

        """
        # Calculate total size of the merged image
        widths, heights = zip(*(img.size for img in self.image_list))
        if self.direction == "x":
            total_width = sum(widths) + self.spacing * (len(self.image_list) - 1)
            max_height = max(heights)
            merged_size = (total_width, max_height)
        elif self.direction == "y":
            total_height = sum(heights) + self.spacing * (len(self.image_list) - 1)
            max_width = max(widths)
            merged_size = (max_width, total_height)

        # Create a new blank image
        merged_image = Image.new("RGBA", merged_size, (255, 255, 255, 0))

        # Paste images onto the merged image
        offset = 0
        for img in self.image_list:
            if self.direction == "x":
                y_offset = 0
                if self.align == "center":
                    y_offset = (max_height - img.height) // 2
                elif self.align == "end":
                    y_offset = max_height - img.height
                merged_image.paste(img, (offset, y_offset))
                offset += img.width + self.spacing
            elif self.direction == "y":
                x_offset = 0
                if self.align == "center":
                    x_offset = (max_width - img.width) // 2
                elif self.align == "end":
                    x_offset = max_width - img.width
                merged_image.paste(img, (x_offset, offset))
                offset += img.height + self.spacing

        return merged_image


if __name__ == "__main__":
    image_list = [
        Image.open(infile)
        for infile in Path(r"C:\Users\aimlo\Desktop\UPLOAD").iterdir()
    ]
    ImageMerge(
        image_list=image_list,
        direction="y",
        spacing=0,
        align="end",
    ).main().show()
