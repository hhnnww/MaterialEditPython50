from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_画册拼接(material_path: str, oneline_count: int = 3):
    def __单个文件夹拼接(sub_path: Path, oneline_count: int) -> Image.Image:
        all_img = rglob(folder=sub_path.as_posix(), suffix=IMAGE_SUFFIX)
        all_img_groups = [
            all_img[i : i + oneline_count]
            for i in range(0, len(all_img), oneline_count)
        ]
        bg_color = (255, 255, 255, 255)
        spacing = 15
        bg_groups = []

        image_list = []
        for oneline in all_img_groups:
            if len(oneline) != oneline_count:
                continue

            for image in oneline:
                im = Image.open(image).convert("RGBA")
                im.thumbnail((300, 300), resample=Image.Resampling.LANCZOS)
                image_list.append(im)

            bg_groups.append(
                fun_图片横向拼接(
                    image_list=image_list,
                    spacing=spacing,
                    align_item="start",
                    background_color=bg_color,
                ),
            )
            image_list = []

        bg = fun_图片竖向拼接(
            image_list=bg_groups,
            spacing=spacing,
            align_item="start",
            background_color=bg_color,
        )

        return fun_图片扩大粘贴(
            im=bg,
            width=bg.width + (spacing * 2),
            height=bg.height + (spacing * 2),
            left="center",
            top="center",
            background_color=bg_color,
        )

    for subpath in Path(material_path).iterdir():
        if subpath.is_dir():
            __单个文件夹拼接(sub_path=subpath, oneline_count=oneline_count).save(
                subpath.parent / f"{subpath.stem}.png",
            )


if __name__ == "__main__":
    fun_画册拼接(
        material_path=r"F:\\小夕素材\11000-11999\11221\11221",
        oneline_count=10,
    )
