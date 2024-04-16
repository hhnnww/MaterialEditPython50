from ..type import _ImageItem


def fun_图片编组(image_list: list[_ImageItem], line_number: int, max_line_ratio: float) -> list[list[_ImageItem]]:
    new_list = []
    in_list = []
    online_ratio = 0
    break_num = 0

    for num, image in enumerate(image_list):
        image: _ImageItem
        in_list.append(image)
        online_ratio += image.ratio

        if (break_num == 0 or num - break_num > 10) and len(in_list) == line_number - 1:
            new_list.append(in_list.copy())
            online_ratio = 0
            in_list = []
            break_num = num + 1

        if num < len(image_list) - 1 and len(in_list) > 0:
            if online_ratio + image_list[num + 1].ratio >= max_line_ratio:
                new_list.append(in_list.copy())
                online_ratio = 0
                in_list = []

        if len(in_list) >= line_number:
            new_list.append(in_list.copy())
            online_ratio = 0
            in_list = []

        if num + 1 == len(image_list) and len(in_list) > 0:
            new_list.append(in_list.copy())

    return new_list
