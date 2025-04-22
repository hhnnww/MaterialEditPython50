"""功能: 实现画册拼接功能

将指定文件夹中的图片按照指定的行数进行拼接，并保存为一张图片。

函数:
- fun_画册拼接(material_path: str, oneline_count: int = 3):
    参数:
        - material_path (str): 素材文件夹的路径，包含需要拼接的图片。
        - oneline_count (int): 每行拼接的图片数量 默认为3。
    功能:
        遍历指定文件夹中的子文件夹，对每个子文件夹中的图片进行拼接，并将拼接结果保存为子文件夹同名的图片。
- __单个文件夹拼接(sub_path: Path, oneline_count: int) -> Image.Image:
    参数:
        - sub_path (Path): 子文件夹路径。
        - oneline_count (int): 每行拼接的图片数量。
    返回:
        - Image.Image: 拼接完成的图片对象。
    功能:
        对单个子文件夹中的图片进行横向和竖向拼接，生成最终的拼接图片。
依赖:
- PIL.Image: 用于图片处理。
- pathlib.Path: 用于文件路径操作。
- 自定义模块:
    - fun_图片扩大粘贴: 用于将图片扩展并粘贴到指定背景上。
    - fun_图片横向拼接: 用于将多张图片横向拼接。
    - fun_图片竖向拼接: 用于将多张图片竖向拼接。
    - rglob: 用于递归遍历指定文件夹中的图片文件。
    - IMAGE_SUFFIX: 图片文件的后缀名设置。
注意:
- 图片会被缩略到300x300像素大小。
- 拼接时会添加15像素的间距 背景颜色为白色 (RGBA: 255, 255, 255, 255)。
- 如果某行图片数量不足指定数量 (oneline_count)，则该行不会被拼接。
- 拼接结果会保存到子文件夹的父目录，文件名为子文件夹名称加.png后缀。
"""

from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_画册拼接(material_path: str, oneline_count: int = 3) -> None:
    """画册拼接。

    fun_画册拼接(material_path: str, oneline_count: int = 3)
    该函数用于对指定路径下的文件夹进行画册拼接操作。
    每个子文件夹中的图片会按照指定的每行图片数量进行横向拼接，
    然后将多行图片竖向拼接，最终生成一个完整的画册图像并保存。
    参数:
        material_path (str): 包含多个子文件夹的主目录路径，
        每个子文件夹中的图片将被拼接。

        oneline_count (int): 每行拼接的图片数量，默认为 3。
    内部函数:
        __单个文件夹拼接(sub_path: Path, oneline_count: int) -> Image.Image:
            对单个子文件夹中的图片进行拼接操作，返回拼接后的图像。
    功能:
        - 遍历主目录下的所有子文件夹。
        - 对每个子文件夹中的图片按照指定数量进行横向拼接。
        - 将多行拼接结果竖向拼接为一个完整的画册。
        - 在画册图像周围添加边距。
        - 将最终生成的画册图像保存到主目录下，文件名为子文件夹名称加 ".png"。
    返回:
        无返回值。拼接后的图像会直接保存到指定路径。
    """

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
