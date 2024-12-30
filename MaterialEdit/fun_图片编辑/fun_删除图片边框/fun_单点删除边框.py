from functools import cached_property
from typing import Optional, Tuple

from PIL import Image


class DelPILBorder:
    def __init__(self, img: Image.Image, border_color: Optional[Tuple[int]]) -> None:
        if img.mode != "RGBA":
            img = img.convert(mode="RGBA")

        self.img = img
        self.border_color = border_color

    @cached_property
    def fun_边框颜色(self):
        if self.border_color is None:
            return self.img.getpixel((0, 0))

        return self.border_color

    @cached_property
    def left(self) -> int:
        for left in range(self.img.width):
            for top in range(self.img.height):
                if self.img.getpixel((left, top)) != self.fun_边框颜色:
                    if left > 0:
                        left -= 1
                    return left

        return 0

    @cached_property
    def upper(self) -> int:
        for top in range(self.img.height):
            for left in range(self.img.width):
                if self.img.getpixel(xy=(left, top)) != self.fun_边框颜色:
                    if top > 1:
                        top -= 1
                    return top
        return 0

    @cached_property
    def right(self) -> int:
        for right in range(self.img.width - 1, 0, -1):
            for top in range(self.img.height):
                if self.img.getpixel(xy=(right, top)) != self.fun_边框颜色:
                    if right < self.img.width:
                        right += 1
                    return right

        return self.img.width

    @cached_property
    def bottom(self) -> int:
        for bottom in range(self.img.height - 1, 0, -1):
            for left in range(self.img.width):
                if self.img.getpixel((left, bottom)) != self.fun_边框颜色:
                    if bottom < self.img.height:
                        bottom += 1
                    return bottom

        return self.img.height

    def main(self) -> Image.Image:
        bbox = (self.left, self.upper, self.right, self.bottom)
        return self.img.crop(box=bbox)
