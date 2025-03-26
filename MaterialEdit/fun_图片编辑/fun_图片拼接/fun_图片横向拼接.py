"""函数功能: 将多张图片横向拼接成一张图片。

参数:
    image_list (list[Image.Image]): 要拼接的图片列表，每个元素为 PIL.Image.Image 对象。
    spacing (int): 图片之间的间距（像素）。
    align_item (ALIGNITEM): 图片的对齐方式，可选值为 "start"（顶部对齐）、
    "center"（居中对齐）或 "end"（底部对齐）。
    background_color (_COLOR): 背景颜色，支持 RGBA 格式。
返回值:
    Image.Image: 拼接后的图片对象。
注意:
    - 图片列表中的每张图片需要是 PIL.Image.Image 对象。
    - 如果 align_item 的值不在指定范围内，函数可能会抛出异常。
"""

from PIL import Image

from MaterialEdit.type import _COLOR, ALIGNITEM


def fun_图片横向拼接(
    image_list: list[Image.Image],
    spacing: int,
    align_item: ALIGNITEM,
    background_color: _COLOR,
) -> Image.Image:
    """函数功能: 将多张图片横向拼接成一张图片。

    参数:
        image_list (list[Image.Image]): 要拼接的图片列表，每个元素为 PIL.Image.Image 对象。
        spacing (int): 图片之间的间距（像素）。
        align_item (ALIGNITEM): 图片的对齐方式，可选值为 "start"（顶部对齐）、
        "center"（居中对齐）或 "end"（底部对齐）。
        background_color (_COLOR): 背景颜色，支持 RGBA 格式。
    返回值:
        Image.Image: 拼接后的图片对象。
    注意:
        - 图片列表中的每张图片需要是 PIL.Image.Image 对象。
        - 如果 align_item 的值不在指定范围内，函数可能会抛出异常。
    """
    width = sum([image.width for image in image_list]) + (
        int((len(image_list) - 1) * spacing)
    )
    height = max([image.height for image in image_list])

    bg = Image.new("RGBA", (width, height), background_color)

    left, top = 0, 0

    for image in image_list:
        if align_item == "start":
            bg.paste(image, (left, top), image)

        elif align_item == "center":
            top = int((bg.height - image.height) / 2)
            bg.paste(image, (left, top), image)

        elif align_item == "end":
            top = bg.height - image.height
            bg.paste(image, (left, top), image)

        left += image.width + spacing
    return bg
