import math
from pathlib import Path

from PIL import Image

from image_action.image_action import ImageAction
from image_action.image_funs import Align
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


def __计算合适的大图尺寸(
    pil_list: list[Image.Image],
) -> list[list[Image.Image]]:
    count = len(pil_list)

    # 获取所有图片的宽高
    sizes = [img.size for img in pil_list]
    widths, heights = zip(*sizes, strict=False)
    avg_w = sum(widths) // count
    avg_h = sum(heights) // count

    # 计算最接近正方形的列数
    best_cols = 1
    min_diff = float("inf")
    for cols in range(1, count + 1):
        rows = math.ceil(count / cols)
        total_w = cols * avg_w
        total_h = rows * avg_h
        diff = abs(total_w - total_h)
        if diff < min_diff:
            min_diff = diff
            best_cols = cols

    rows = math.ceil(count / best_cols)
    return [pil_list[i * best_cols : (i + 1) * best_cols] for i in range(rows)]


def fun_制作版权图片(preview_path: str, design_path: str) -> None:
    iamge_file = [
        infile
        for infile in rglob(preview_path, suffix=IMAGE_SUFFIX)
        if "_thumb" not in infile.stem
    ]

    pil_list = [
        ImageAction.open_image(infile.as_posix()).convert("RGBA")
        for infile in iamge_file
    ]

    bg = ImageAction.fun_图片竖向拼接(
        image_list=[
            ImageAction.fun_图片横向拼接(
                image_list=row_list,
                spacing=200,
                align="start",
            )
            for row_list in __计算合适的大图尺寸(pil_list)
        ],
        spacing=200,
        align="start",
    )

    design_path_obj = Path(design_path)
    if not design_path_obj.exists():
        design_path_obj.mkdir(parents=True, exist_ok=True)

    ImageAction.fun_图片添加背景(
        im=ImageAction.fun_图片扩大(
            im=bg,
            size=(bg.width + 400, bg.height + 400),
            left_align=Align.CENTER,
            right_align=Align.CENTER,
        ),
        bg_color=(255, 255, 255, 255),
    ).convert("RGB").save(design_path_obj / "版权图片.jpg", quality=80, optimize=True)


if __name__ == "__main__":
    preview_path = r"F:\泡泡素材\3000-3999\3482\预览图"
    design_path = r"F:\泡泡素材\3000-3999\3482\设计图"
    fun_制作版权图片(preview_path, design_path)
