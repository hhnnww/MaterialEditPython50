from PIL import Image

from ..type import _ImageItem
from tqdm import tqdm


def fun_构建图片(image_list: list[str]) -> list[_ImageItem]:
    l = []

    for image in tqdm(image_list, desc="构建图片列表", ncols=100):
        try:
            with Image.open(image) as im:
                l.append(_ImageItem(path=image, width=im.width, height=im.height, ratio=im.width / im.height))
        except ValueError as e:
            print(image, e)

    return l
