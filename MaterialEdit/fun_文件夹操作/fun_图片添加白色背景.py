from pathlib import Path

from PIL import Image
from tqdm import tqdm

from .fun_遍历指定文件 import rglob


def fun_图片添加白色背景(material_path_text: str):
    material_path = Path(material_path_text)
    png_file_list = rglob(material_path.as_posix(), [".png"])
    for in_png in tqdm(png_file_list, ncols=100, desc="图片添加白色背景"):
        print(in_png)
        with Image.open(in_png.as_posix()) as im:
            if im.mode != "RGBA":
                im = im.convert("RGBA")

            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            bg.paste(im, (0, 0), im)
            bg.save(in_png.as_posix())
            bg.close()
