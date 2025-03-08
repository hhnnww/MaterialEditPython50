import math

from PIL import Image

from MaterialEdit.type import _COLOR, ALIGNITEM


def fun_图片竖向拼接(
    image_list: list[Image.Image],
    spacing: int,
    align_item: ALIGNITEM,
    background_color: _COLOR,
) -> Image.Image:
    width = max([image.width for image in image_list])
    height = sum([image.height for image in image_list]) + int(
        (len(image_list) - 1) * spacing,
    )

    bg = Image.new("RGBA", (width, height), background_color)

    left, top = 0, 0

    for image in image_list:
        if align_item == "start":
            bg.paste(image, (left, top), image)

        elif align_item == "center":
            left = math.ceil((bg.width - image.width) / 2)
            bg.paste(image, (left, top), image)

        elif align_item == "end":
            left = bg.width - image.width
            bg.paste(image, (left, top), image)

        top += image.height + spacing

    return bg
