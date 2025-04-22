"""使用IBM字体生成单行文字"""

from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont

from MaterialEdit.fun_图片编辑.fun_删除图片边框.fun_删除图片边框 import fun_删除图片边框
from MaterialEdit.type import _COLOR


class MakeIbmFont:
    """使用ibm字体生成图片"""

    def __init__(
        self,
        text: str,
        size: int,
        weight: Literal[
            "thin",
            "extralight",
            "light",
            "regular",
            "text",
            "medium",
            "semibold",
            "bold",
        ],
        color: _COLOR,
        bg_color: _COLOR,
    ) -> None:
        self.text = text
        self.size = size
        self.weight = weight
        self.color = color
        self.bg_color = bg_color

    @property
    def get_font_path(self) -> Path:
        font_dir = Path(__file__).parent / "ibm-plex-sans"
        return font_dir / f"IBMPlexSansSC-{self.weight}.ttf"

    @property
    def __true_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(font=self.get_font_path, size=self.size)

    @property
    def get_size(self) -> tuple[int, int]:
        bbox = self.__true_font.getbbox(text=self.text)
        width = int(bbox[2])
        height = int(bbox[3])
        return (width, height)

    def main(self) -> Image.Image:
        """生成单行文字"""
        bg = Image.new(mode="RGBA", size=self.get_size, color=self.bg_color)
        draw = ImageDraw.Draw(im=bg)
        draw.text(xy=(0, 0), text=self.text, font=self.__true_font, fill=self.color)
        return fun_删除图片边框(im=bg)


if __name__ == "__main__":
    obj = MakeIbmFont(
        text="288套 2025蛇年海报",
        size=200,
        weight="thin",
        color=(255, 255, 255, 255),
        bg_color=(80, 80, 80, 255),
    )
    obj.main().show()
