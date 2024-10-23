from pathlib import Path

from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_文件夹操作.fun_获取二维码 import fun_获取二维码

from ..fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import fun_单行文字转图片
from ..fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from ..fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from ..fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from ..fun_遍历图片 import fun_遍历图片


def fun_素材图水印(material_path: str, shop_name: str):
    erweima_pil = fun_获取二维码(shop_name=shop_name)

    water_pix_color = int(255)
    shop_name_pil = fun_单行文字转图片(
        text=shop_name,
        chinese_font_name="noto",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=250,
        fill_color=(255, 255, 255, 255),
        background_color=(255, 255, 255, 0),
    )
    spacing = 30
    t2 = ""
    t3 = ""
    match shop_name:
        case "小夕素材":
            t2 = "xdscp.taobao.com"
            t3 = "9.9元加入会员，全店免费"
        case "泡泡素材":
            t2 = "paopaosucai.taobao.com"
            t3 = "9.9元加入会员，全店免费"
        case "饭桶设计":
            t2 = "ftdesign.taobao.com"

    t2_pil = fun_单行文字转图片(
        text=t2,
        chinese_font_name="noto",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=120,
        fill_color=(255, 255, 255, 255),
        background_color=(255, 255, 255, 0),
    )

    t3_pil = fun_单行文字转图片(
        text=t3,
        chinese_font_name="noto",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=120,
        fill_color=(255, 255, 255, 255),
        background_color=(255, 255, 255, 0),
    )

    shop_name_pil = fun_图片竖向拼接(
        [shop_name_pil, t2_pil, t3_pil], spacing, "start", (255, 255, 255, 0)
    )
    water_pil = fun_获取单个水印(
        600, (water_pix_color, water_pix_color, water_pix_color, water_pix_color)
    )
    water_pil = fun_图片竖向拼接(
        [water_pil, shop_name_pil], spacing, "start", (255, 255, 255, 0)
    )
    water_pil.thumbnail((999999, erweima_pil.height), resample=Image.Resampling.LANCZOS)

    water_pil = fun_图片横向拼接(
        [erweima_pil, water_pil], spacing, "start", (255, 255, 255, 0)
    )

    all_image = fun_遍历图片(folder=material_path, used_image_number=0, image_sort=True)

    im_width = 2000
    for in_file_stem in tqdm(all_image, ncols=100, desc="素材图水印\t"):
        in_file: Path = Path(in_file_stem)

        if shop_name in in_file.stem:
            try:
                im = Image.open(in_file.as_posix())

                im.thumbnail((im_width, im_width), Image.Resampling.LANCZOS, 3)
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
