from PIL import Image

from ..type import ImageModel


def fun_重新构建所有图片(image_list: list[ImageModel]):
    l = []
    for obj in image_list:
        with Image.open(obj.path) as im:
            print(obj.path)
            ratio = im.width / im.height
            if ratio < 0.2:
                ratio = 0.2

            l.append(ImageModel(path=obj.path, ratio=ratio))
    return l
