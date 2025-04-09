"""layout 一大周围小"""

from pathlib import Path
from secrets import randbelow

from PIL import Image
from tomorrow3 import threads
from tqdm import tqdm

from MaterialEdit.fun_图片编辑.fun_预览图水印.fun_单个预览图效果图水印 import (
    fun_单个预览图效果图水印,
)
from MaterialEdit.fun_遍历图片 import fun_遍历图片


@threads(10)
def __单个文件处理(file: Path, logo: Image.Image) -> None:
    with Image.open(file.as_posix()) as im:
        max_height_ratio = 4
        if im.height / im.width > max_height_ratio:
            im = im.crop((0, 0, im.width, im.width * max_height_ratio))

        im.thumbnail((2000, 2000))
        random_number = randbelow(100) + 1
        if random_number % 2 == 1:  # Odd number
            position = (50, im.height - logo.height - 50)
        else:  # Even number
            position = (im.width - logo.width - 50, im.height - logo.height - 50)

        # Paste the logo at the determined position
        im.paste(logo, position, logo)
        im.save(file.as_posix())


def fun_素材图水印2(material_path: str, shop_name: str) -> None:
    """素材图水印"""
    logo = fun_单个预览图效果图水印(
        shop_name=shop_name,
        cate="ylt",
    )
    logo_max_size = 400
    logo.thumbnail((logo_max_size, logo_max_size))

    for file in tqdm(
        [
            in_file
            for in_file in fun_遍历图片(
                folder=material_path,
                used_image_number=0,
                image_sort=True,
            )
            if in_file.parent.stem.lower() not in ["links"]
        ],
        desc="素材图水印",
        ncols=100,
    ):
        __单个文件处理(file=file, logo=logo)


if __name__ == "__main__":
    logo = fun_单个预览图效果图水印(
        shop_name="小夕素材",
        cate="ylt",
    )
    logo_max_size = 500
    logo.thumbnail((logo_max_size, logo_max_size))
    __单个文件处理(
        file=Path(
            r"F:\BaiduNetdiskDownload\0-饭桶设计\03481-异形挂件样机\黑鲸大礼包\贴图样机教程.jpg",
        ),
        logo=logo,
    )
