from pathlib import Path

from PIL import Image

from ...type import _COLOR


def fun_获取单个水印(size: int, fill_clor: _COLOR):
    water_mark_path = Path(__file__).parent.parent / "logo.png"
    water_mark_pil = Image.open(water_mark_path.as_posix())
    with Image.new("RGBA", water_mark_pil.size, fill_clor) as fill_bg:
        water_mark_pil.paste(fill_bg, (0, 0), water_mark_pil)

    water_mark_pil.thumbnail(
        (size, size), resample=Image.LANCZOS, reducing_gap=3
    )
    # text_pil = run_单行文字转图片(
    #     text="小夕素材",
    #     chinese_font_name="zihun",
    #     english_font_name="zihun",
    #     font_weight="heavy",
    #     font_size=100,
    #     fill_color=fill_clor,
    #     background_color=(255, 255, 255, 0),
    #     en_size_expand_ratio=1,
    # )
    #
    # text_large_ratio = 1.8
    # text_pil.thumbnail((int(size * text_large_ratio), int(size * text_large_ratio)), Image.LANCZOS, 3)
    # im = run_图片竖向拼接(
    #     [water_mark_pil, text_pil], spacing=int(size * 0.2), background_color=(255, 255, 255, 0), align_item="center"
    # )

    return water_mark_pil
