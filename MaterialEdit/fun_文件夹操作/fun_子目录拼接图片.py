"""文件重命名.py"""

from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


def fun_子目录拼接图片(material_path: str) -> None:
    """子目录拼接图片."""

    def __内目录拼接图片(in_path: Path) -> Image.Image:
        all_pic = rglob(
            folder=in_path.as_posix(),
            suffix=[".jpeg", ".png", ".jpg"],
        )

        all_pil = []
        for in_file in all_pic:
            im = Image.open(in_file)
            im = im.convert("RGBA")
            im = fun_图片裁剪(
                im=im,
                width=800,
                height=int(800 / (im.width / im.height)),
                position="center",
            )
            all_pil.append(im)

        # 计算图片比例
        ratio = sum([pil.width / pil.height for pil in all_pil]) / len(all_pil)

        if ratio < 0.7:
            bg = fun_图片横向拼接(
                image_list=all_pil,
                spacing=10,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )

        else:
            bg = fun_图片竖向拼接(
                image_list=all_pil,
                spacing=0,
                align_item="start",
                background_color=(255, 255, 255, 255),
            )

        return bg

    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            png_path = Path(material_path) / f"{in_path.stem}.png"
            if png_path.exists() is not True:
                im = __内目录拼接图片(in_path=in_path)
                im.save(png_path.as_posix())
