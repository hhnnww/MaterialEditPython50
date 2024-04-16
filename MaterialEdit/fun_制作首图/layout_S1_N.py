from ..type import ImageModel
from ..fun_图片编辑 import ImageEdit
from PIL import Image
from tqdm import tqdm


def layout_s1_n(image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int, col: int) -> Image.Image:
    single_col = (xq_width - ((col + 3) * spacing)) / (col + 2)

    large_image_width = ((single_col * 2) + spacing) * 0.9
    large_image_height = xq_height - (spacing * 2)

    large_im = Image.open(image_list[0].path)
    large_im = ImageEdit.fun_图片裁剪(large_im, int(large_image_width), int(large_image_height), position="center")

    small_im_height = (xq_height - (spacing * 3)) / 2

    left, top = spacing, spacing
    bg = Image.new("RGBA", (xq_width, xq_height), (255, 255, 255, 255))
    if spacing > 0:
        large_im = ImageEdit.fun_图片画边框(large_im, (240, 240, 240, 255))
        large_im = ImageEdit.fun_图片切换到圆角(large_im, 15, (255, 255, 255, 255))
    bg.paste(large_im, (left, top))

    left = left + large_im.width + spacing

    num = 0
    small_width = (xq_width - large_image_width - (spacing * (col + 2))) / col
    for small_im in tqdm(image_list[1:], ncols=100, desc="制作首图"):
        im = Image.open(small_im.path)
        im = ImageEdit.fun_图片裁剪(im, width=int(small_width), height=int(small_im_height), position="center")
        if spacing > 0:
            im = ImageEdit.fun_图片画边框(im, (240, 240, 240, 255))
            im = ImageEdit.fun_图片切换到圆角(im, 15, (255, 255, 255, 255))
        bg.paste(im, (int(left), top))
        left = left + im.width + spacing

        if left >= bg.width - spacing:
            left = large_image_width + int(spacing * 2)
            top += im.height + spacing

        num += 1

        if num == col * 2:
            break

    return bg
