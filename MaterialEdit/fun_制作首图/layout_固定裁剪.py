from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪

from ..setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO
from ..type import ALIGNITEM, ImageModel


def fun_固定裁剪(
    xq_width: int,
    xq_height: int,
    image_list: list[ImageModel],
    line: int,
    spacing: int,
    crop_position: ALIGNITEM,
):
    one_line_height = int((xq_height - ((line + 1) * spacing)) / line)

    line_ratio_list = []
    for x in range(1, 8):
        small_im_width = int((xq_width - ((x + 1) * spacing)) / x)
        ratio = small_im_width / one_line_height
        line_ratio_list.append((x, ratio))

    image_average_ratio = sum([obj.ratio for obj in image_list]) / len(image_list)

    best_ratio_list = [
        (obj[0], abs(obj[1] - image_average_ratio)) for obj in line_ratio_list
    ]
    best_ratio_list.sort(key=lambda k: k[1], reverse=False)

    best_ratio_sort_list = best_ratio_list[0]
    best_ratio = best_ratio_sort_list[0]

    small_im_width = int((xq_width - ((best_ratio + 1) * spacing)) / best_ratio)

    bg = Image.new("RGBA", (xq_width, xq_height), (255, 255, 255, 255))
    left, top = spacing, spacing

    image_list.sort(key=lambda k: abs(k.ratio - best_ratio_sort_list[1]), reverse=False)

    num = 0
    for image in tqdm(image_list[: best_ratio * line], ncols=100, desc="制作首图\t"):
        im = Image.open(image.path)
        if im.mode != "RGBA":
            im = im.convert("RGBA")

        im = fun_图片裁剪(im, small_im_width, one_line_height, crop_position)

        if spacing > 0:
            im = fun_图片画边框(im, FIRST_IMAGE_BORDER_COLOR)
            im = fun_图片切换到圆角(im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

        bg.paste(im, (left, top), im)
        left += im.width + spacing + 1

        num += 1
        if num == best_ratio:
            num = 0
            top += im.height + spacing
            left = spacing

        im.close()

    return bg


def fun_列表分段(image_list: list[str], row: int, col: int):
    img_list = []
    inline = []
    for in_image in image_list:
        inline.append(in_image)
        if len(inline) == row:
            img_list.append(inline.copy())
            inline = []

        if len(img_list) == col:
            return img_list
