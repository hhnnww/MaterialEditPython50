from itertools import combinations

from PIL import Image
from pydantic import BaseModel
from tqdm import tqdm

from .fun_重新构建所有图片 import fun_重新构建所有图片
from ..fun_图片编辑 import ImageEdit
from ..setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO
from ..type import ImageModel, ALIGNITEM


class CombList(BaseModel):
    ratio: float
    image_list: list[ImageModel]
    diff: float


class LayoutAdaptiveCrop:
    def __init__(
        self,
        image_list: list[ImageModel],
        xq_width: int,
        xq_height: int,
        line: int,
        spacing: int,
        crop_position: ALIGNITEM,
    ):
        self.image_list = fun_重新构建所有图片(image_list)
        self.xq_width = xq_width
        self.xq_height = xq_height
        self.line = line
        self.spacing = spacing
        self.crop = crop_position

        self.online_height = int((self.xq_height - ((self.line + 1) * self.spacing)) / self.line)

    def fun_构建所有组合(self):
        oneline_ratio = self.fun_计算单行比例()
        comb_image_list = []
        for x in range(1, 6):
            for in_line in combinations(self.image_list, x):
                ratio = sum([obj.ratio for obj in in_line])
                comb_image_list.append(CombList(image_list=in_line, ratio=ratio, diff=abs(oneline_ratio - ratio)))

        comb_image_list.sort(key=lambda k: k.diff, reverse=False)
        return comb_image_list

    def fun_计算单行比例(self):
        online_height = int((self.xq_height - ((self.line + 1) * self.spacing)) / self.line)
        return self.xq_width / online_height

    def fun_构建首图组合(self):
        used_comb_list = []
        used_image = []

        for comb_list in self.fun_构建所有组合():
            comb_used = False
            for in_item in comb_list.image_list:
                if in_item.path in used_image:
                    comb_used = True

            if not comb_used:
                used_comb_list.append(comb_list)
                for in_item in comb_list.image_list:
                    used_image.append(in_item.path)

            if len(used_comb_list) == self.line:
                return used_comb_list

    def fun_制作单行(self, comb_list: CombList):
        all_pil = []
        col_width = int(
            (self.xq_width - ((len(comb_list.image_list) + 1) * self.spacing))
            / sum([obj.ratio for obj in comb_list.image_list])
        )
        for image in comb_list.image_list:
            im = Image.open(image.path)
            im = ImageEdit.fun_图片裁剪(im, int(col_width * image.ratio), self.online_height, self.crop)
            if self.spacing > 0:
                im = ImageEdit.fun_图片画边框(im, FIRST_IMAGE_BORDER_COLOR)
                im = ImageEdit.fun_图片切换到圆角(im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))
            all_pil.append(im)

        return ImageEdit.fun_图片横向拼接(all_pil, self.spacing, "start", (255, 255, 255, 255))

    def run_制作自适应布局图片(self):
        all_pil = []
        for comb_list in tqdm(self.fun_构建首图组合(), ncols=100, desc="制作首图\t"):
            all_pil.append(self.fun_制作单行(comb_list))

        bg = ImageEdit.fun_图片竖向拼接(all_pil, self.spacing, "start", (255, 255, 255, 255))
        bg = ImageEdit.fun_图片扩大粘贴(
            bg,
            width=self.xq_width,
            height=self.xq_height,
            left="center",
            top="center",
            background_color=(255, 255, 255, 255),
        )
        return bg
