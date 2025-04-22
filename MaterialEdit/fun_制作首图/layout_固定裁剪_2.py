"""固定裁剪."""

from __future__ import annotations

import math
from itertools import cycle
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from tqdm import tqdm

from image_action.image_action import ImageAction
from MaterialEdit.fun_制作首图.fun_重新构建所有图片 import fun_重新构建所有图片

if TYPE_CHECKING:
    from MaterialEdit.type import ALIGNITEM, ImageModel


def fun_layout_固定裁剪2(  # noqa: PLR0913
    xq_width: int,
    xq_height: int,
    image_list: list[ImageModel],
    line: int,
    spacing: int,
    crop_position: ALIGNITEM,
    design_path: str,
) -> Image.Image:
    """固定裁剪."""
    image_list = fun_重新构建所有图片(image_list)

    # 计算所有图片的平均比例
    all_image_average_ratio = sum(
        [image.ratio for image in image_list if image.ratio is not None],
    ) / len(image_list)

    image_list = cycle(image_list)  # type: ignore  # noqa: PGH003

    # 计算单行各种图片的比例
    oneline_num_ratio_list = fun_计算单行所有图片数量的比例(
        line,
        xq_width,
        xq_height,
        spacing,
    )

    for obj in oneline_num_ratio_list:
        obj.append(abs(all_image_average_ratio - obj[1]))

    oneline_num_ratio_list.sort(key=lambda k: k[2], reverse=False)

    row = oneline_num_ratio_list[0][0]
    image_comb_list = fun_列表分段(image_list, row, line)

    image_height = math.ceil((xq_height - ((line + 1) * spacing)) / line)
    image_width = math.ceil((xq_width - ((row + 1) * spacing)) / row)

    all_comb = []

    for comb_list in tqdm(image_comb_list, ncols=100, desc="制作首图\t"):
        one_line = []

        if comb_list:
            for image in comb_list:
                im = Image.open(image.path).convert("RGBA")

                if im.mode != "RGBA":
                    im = im.convert("RGBA")

                im = ImageAction.fun_图片裁剪(
                    im,
                    (image_width, image_height),
                    crop_position,
                )

                one_line.append(im)

        one_line_im = ImageAction.fun_图片横向拼接(
            one_line,
            spacing,
            "center",
        )

        all_comb.append(one_line_im)

    bg = ImageAction.fun_图片竖向拼接(all_comb, spacing, "center")
    bg = bg.resize((xq_width, xq_height), Image.Resampling.LANCZOS)

    if Path(design_path).exists() is not True:
        Path(design_path).mkdir()

    design_image_name = f"{len(list(Path(design_path).iterdir()))}.png"
    bg.save(fp=f"{Path(design_path)}/{design_image_name}")

    return bg


def fun_列表分段(
    image_list: list[ImageModel],
    row: float,
    col: int,
) -> list[list[ImageModel]] | None:
    """列表分段."""
    left = []
    inline = []
    for in_image in image_list:
        inline.append(in_image)
        if len(inline) == row:
            left.append(inline.copy())
            inline = []

        if len(left) == col:
            return left

    return None


def fun_计算单行所有图片数量的比例(
    line: int,
    xq_width: int,
    xq_height: int,
    spacing: int,
) -> list[list[int | float]]:
    """计算图片比例."""
    comb_list = []
    oneline_height = int((xq_height - ((line + 1) * spacing)) / line)
    for x in range(1, 10):
        small_image_width = int((xq_width - ((x + 1) * spacing)) / x)
        ratio = small_image_width / oneline_height
        comb_list.append([x, ratio])
    return comb_list
