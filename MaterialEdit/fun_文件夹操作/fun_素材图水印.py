from pathlib import Path

from PIL import Image
from pypinyin import lazy_pinyin
from tqdm import tqdm

from ..fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import fun_单行文字转图片
from ..fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from ..fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from ..fun_遍历图片 import fun_遍历图片


def fun_素材图水印(material_path: str, shop_name: str):
    water_pix_color = int(255)
    shop_name_pil = fun_单行文字转图片(
        text=shop_name,
        chinese_font_name="zihun",
        english_font_name="montserrat",
        font_weight="bold",
        font_size=25,
        fill_color=(255, 255, 255, 255),
        background_color=(255, 255, 255, 0),
    )
    shop_name_pinyin = fun_单行文字转图片(
        text="".join(lazy_pinyin(shop_name)),
        chinese_font_name="misans",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=10,
        fill_color=(255, 255, 255, 255),
        background_color=(255, 255, 255, 0),
    )
    shop_name_pil = fun_图片竖向拼接(
        [shop_name_pil, shop_name_pinyin], 5, "center", (255, 255, 255, 0)
    )
    water_pil = fun_获取单个水印(
        60, (water_pix_color, water_pix_color, water_pix_color, water_pix_color)
    )
    water_pil = fun_图片竖向拼接(
        [water_pil, shop_name_pil], 10, "center", (255, 255, 255, 0)
    )

    all_image = fun_遍历图片(folder=material_path, used_image_number=0, image_sort=True)

    for in_file_stem in tqdm(all_image, ncols=100, desc="素材图水印\t"):
        in_file: Path = Path(in_file_stem)

        if shop_name in in_file.stem:
            try:
                im = Image.open(in_file.as_posix())

                im.thumbnail((1200, 1200), Image.Resampling.LANCZOS, 3)
                try:
                    im.paste(
                        water_pil, (20, im.height - water_pil.height - 20), water_pil
                    )
                except OSError:
                    print(in_file.as_posix())
                else:
                    if in_file.suffix.lower() != ".png":
                        im.convert("RGB")

                    im.save(in_file)
                    im.close()
            except ValueError as e:
                print(in_file.as_posix(), e)
