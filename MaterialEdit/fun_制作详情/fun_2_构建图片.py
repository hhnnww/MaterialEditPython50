from PIL import Image
from tqdm import tqdm

from ..type import _ImageItem


def fun_构建图片(image_list: list[str]) -> list[_ImageItem]:
    left = []

    for image in tqdm(image_list, desc="构建图片列表", ncols=100):
        try:
            with Image.open(image) as im:
                left.append(
                    _ImageItem(
                        path=image,
                        width=im.width,
                        height=im.height,
                        ratio=im.width / im.height,
                    )
                )
        except ValueError as e:
            print(image, e)

    return left
