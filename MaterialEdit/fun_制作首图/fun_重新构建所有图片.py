"""构建所有图片."""

from PIL import Image

from MaterialEdit.type import ImageModel


def fun_重新构建所有图片(image_list: list[ImageModel]) -> list[ImageModel]:
    """构建所有图片."""
    img_list = []
    for obj in image_list:
        with Image.open(obj.path) as im:
            ratio = im.width / im.height
            ratio = max(ratio, 0.2)

            img_list.append(ImageModel(path=obj.path, ratio=ratio))

    return img_list
