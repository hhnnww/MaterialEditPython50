import math
from functools import cached_property

from PIL import Image, ImageDraw, ImageFont


class FontToPNG:
    def __init__(self, font_path: str, text: str) -> None:
        self.font_path = font_path
        self.text = text
        self.size = 1000

    @cached_property
    def _fun_true_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(font=self.font_path, size=self.size)

    @cached_property
    def _font_size(self) -> tuple[int, int]:
        size = self._fun_true_font.getbbox(text=self.text)
        return (math.ceil(size[2]), math.ceil(size[3]))

    def _fun_bg(self) -> Image.Image:
        bg = Image.new("RGBA", self._font_size, (255, 255, 255, 0))
        return bg

    def main(self):
        bg = self._fun_bg()
        draw = ImageDraw.Draw(im=bg, mode="RGBA")
        try:
            draw.text((0, 0), self.text, fill=(0, 0, 0, 255), font=self._fun_true_font)
        except:
            pass
        else:
            return bg

        return None


if __name__ == "__main__":
    from pathlib import Path

    for in_file in Path(r"F:\小夕素材\10000-20000\10720\10720").iterdir():
        if in_file.is_file() and in_file.suffix.lower() in [".ttf", ".otf", ".ttc"]:
            for text in ["如雨春秋"]:
                ftp = FontToPNG(in_file.as_posix(), text).main()
                if ftp is not None:
                    ftp.save(rf"C:\Users\aimlo\Desktop\UPLOAD\{in_file.stem}.png")
