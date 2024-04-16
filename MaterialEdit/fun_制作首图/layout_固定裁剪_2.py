from PIL import Image
from tqdm import tqdm

from ..fun_图片编辑.ClassImageEdit import ImageEdit
from ..type import ALIGNITEM, ImageModel
from .fun_重新构建所有图片 import fun_重新构建所有图片


def fun_layout_固定裁剪2(
    xq_width: int,
    xq_height: int,
    image_list: list[ImageModel],
    line: int,
    spacing: int,
    crop_position: ALIGNITEM,
):
    image_list = fun_重新构建所有图片(image_list)

    # 计算所有图片的平均比例
    all_image_average_ratio = sum([image.ratio for image in image_list]) / len(
        image_list
    )

    # 计算单行各种图片的比例
    oneline_num_ratio_list = list(
        fun_计算单行所有图片数量的比例(line, xq_width, xq_height, spacing)
    )

    for obj in oneline_num_ratio_list:
        obj.append(abs(all_image_average_ratio - obj[1]))
        print(obj)

    oneline_num_ratio_list.sort(key=lambda k: k[2], reverse=False)

    row = oneline_num_ratio_list[0][0]
    image_comb_list = fun_列表分段(image_list, row, line)

    image_height = int((xq_height - ((line + 1) * spacing)) / line)
    image_width = int((xq_width - ((row + 1) * spacing)) / row)

    all_comb = []
    for comb_list in tqdm(image_comb_list, ncols=100, desc="制作首图\t"):
        one_line = []
        for image in comb_list:
            im = Image.open(image.path)
            if im.mode != "RGBA":
                im = im.convert("RGBA")

            im = ImageEdit.fun_图片裁剪(im, image_width, image_height, crop_position)
            if spacing > 0:
                im = ImageEdit.fun_图片画边框(im, border_color=(240, 240, 240, 255))
                im = ImageEdit.fun_图片切换到圆角(im, 15, (255, 255, 255, 255))

            one_line.append(im)

        one_line_im = ImageEdit.fun_图片横向拼接(
            one_line, spacing, "center", (255, 255, 255, 255)
        )
        all_comb.append(one_line_im)

    bg = ImageEdit.fun_图片竖向拼接(all_comb, spacing, "center", (255, 255, 255, 255))
    bg = ImageEdit.fun_图片扩大粘贴(
        bg, xq_width, xq_height, "center", "center", (255, 255, 255, 255)
    )
    return bg


def fun_列表分段(image_list: list[ImageModel], row: int, col: int):
    l = []
    inline = []
    for in_image in image_list:
        inline.append(in_image)
        if len(inline) == row:
            l.append(inline.copy())
            inline = []

        if len(l) == col:
            return l


def fun_计算单行所有图片数量的比例(
    line: int, xq_width: int, xq_height: int, spacing: int
):
    oneline_height = int((xq_height - ((line + 1) * spacing)) / line)
    for x in range(1, 10):
        small_image_width = int((xq_width - ((x + 1) * spacing)) / x)
        ratio = small_image_width / oneline_height
        yield [x, ratio]
