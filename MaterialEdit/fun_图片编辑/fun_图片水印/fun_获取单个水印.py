from pathlib import Path

from PIL import Image

from MaterialEdit.type import _COLOR


def fun_获取单个水印(size: int, fill_clor: _COLOR) -> Image.Image:
    """获取单个水印"""
    water_mark_path = Path(__file__).parent.parent / "logo.png"
    water_mark_pil = Image.open(water_mark_path.as_posix())

    with Image.new("RGBA", water_mark_pil.size, fill_clor) as fill_bg:
        water_mark_pil.paste(fill_bg, (0, 0), water_mark_pil)

    water_mark_pil.thumbnail(
        (size, size),
        resample=Image.Resampling.LANCZOS,
        reducing_gap=3,
    )

    return water_mark_pil
