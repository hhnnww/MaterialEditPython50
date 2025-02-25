from PIL import Image

from MaterialEdit.type import _COLOR, ALIGNITEM


def fun_图片横向拼接(
    image_list: list[Image.Image],
    spacing: int,
    align_item: ALIGNITEM,
    background_color: _COLOR,
) -> Image.Image:
    width = sum([image.width for image in image_list]) + (
        int((len(image_list) - 1) * spacing)
    )
    height = max([image.height for image in image_list])

    bg = Image.new("RGBA", (width, height), background_color)

    left, top = 0, 0

    for image in image_list:
        if align_item == "start":
            bg.paste(image, (left, top))

        elif align_item == "center":
            top = int((bg.height - image.height) / 2)
            bg.paste(image, (left, top))

        elif align_item == "end":
            top = bg.height - image.height
            bg.paste(image, (left, top))

        left += image.width + spacing

        image.close()

    return bg
