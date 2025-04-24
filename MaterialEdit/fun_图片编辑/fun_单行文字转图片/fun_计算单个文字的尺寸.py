from PIL import ImageFont

from MaterialEdit.type import _FontSize


def fun_计算单个文字的尺寸(text: str, true_font: ImageFont.FreeTypeFont) -> _FontSize:
    bbox = true_font.getbbox(text=text)
    return _FontSize(width=bbox[2], height=bbox[3])  # type: ignore


if __name__ == "__main__":
    from pathlib import Path

    font_path = Path(__file__).parent / "font" / "misans" / "MiSans-Bold.ttf"
    font_path_obj = ImageFont.truetype(font=font_path.as_posix(), size=100)
    print(fun_计算单个文字的尺寸(text="a", true_font=font_path_obj))
