from PIL import Image
from ..type import ImageModel
from ..fun_图片编辑 import ImageEdit


def fun_layout_1_3(image_list: list[ImageModel], xq_width: int, xq_height: int, spacing: int):
    small_width = int((xq_width - ((3 + 1) * spacing)) / 3)
    small_height = int((xq_height - ((3 + 1) * spacing)) / 3)

    pil_list = []
    for num, image in enumerate(image_list):
        im = Image.open(image.path)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")

        if num == 0:
            im = ImageEdit.fun_图片裁剪(
                im,
                width=int(small_width * 3) + int(spacing * 2),
                height=int(small_height * 2) + int(spacing * 2),
                position="center",
            )
        else:
            im = ImageEdit.fun_图片裁剪(im, width=small_width, height=small_height, position="center")

        if spacing > 0:
            im = ImageEdit.fun_图片画边框(im, (240, 240, 240, 255))
            im = ImageEdit.fun_图片切换到圆角(im, 15, (255, 255, 255, 255))

        pil_list.append(im)

        if len(pil_list) == 4:
            break

    top_pil = pil_list[0]

    two_pil = ImageEdit.fun_图片横向拼接(pil_list[1:4], spacing, "center", (255, 255, 255, 255))

    bg = ImageEdit.fun_图片竖向拼接([top_pil, two_pil], spacing, "start", (255, 255, 255, 255))
    bg = ImageEdit.fun_图片扩大粘贴(bg, xq_width, xq_height, "center", "center", (255, 255, 255, 255))

    return bg
