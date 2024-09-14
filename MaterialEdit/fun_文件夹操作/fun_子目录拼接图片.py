from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件


def fun_子目录拼接图片(material_path: str):
    def __内目录拼接图片(in_path: Path):
        all_pic = fun_遍历指定文件(
            folder=in_path.as_posix(), suffix=[".jpeg", ".png", ".jpg"]
        )

        all_pil = []
        for in_file in all_pic:
            im = Image.open(in_file)
            im = im.convert("RGBA")
            # im.thumbnail((800, 99999))
            im = fun_图片裁剪(
                im=im,
                width=800,
                height=int(800 / (im.width / im.height)),
                position="center",
            )
            all_pil.append(im)

        bg = fun_图片竖向拼接(
            image_list=all_pil,
            spacing=0,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

        return bg

    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            png_path = Path(material_path) / f"{in_path.stem}.png"
            if png_path.exists() is not True:
                im = __内目录拼接图片(in_path=in_path)
                im.save(png_path.as_posix())
