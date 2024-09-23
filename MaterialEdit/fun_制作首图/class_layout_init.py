import math

from PIL import Image
from tqdm import tqdm

from MaterialEdit.type import ImageModel


class LayoutInit:
    def __init__(
        self,
        image_list: list[ImageModel],
        xq_width: int,
        xq_height: int,
        spacing: int,
        col: int,
    ) -> None:
        self.image_list = image_list
        self.xq_width = xq_width
        self.xq_height = xq_height
        self.spacing = spacing
        self.col = col

    @property
    def pil_list(self) -> list[Image.Image]:
        pil_list = []
        for image in tqdm(self.image_list, desc="制作首图布局", ncols=100):
            im = Image.open(image.path)
            if im.mode.lower() != "rgba":
                im = im.convert("RGBA")

            pil_list.append(im)

            if len(pil_list) >= 50:
                break

        return pil_list

    @staticmethod
    def fun_计算小图高度(im: Image.Image, ori_width: int) -> int:
        return math.ceil(ori_width / (im.width / im.height))

    def fun_计算单行高度(self, im_list: list[Image.Image]) -> int:
        return sum([im.height for im in im_list]) + ((len(im_list) - 1) * self.spacing)
