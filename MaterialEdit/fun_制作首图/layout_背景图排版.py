from PIL import Image

from MaterialEdit.fun_图片编辑 import fun_图片裁剪

from .class_layout_init import LayoutInit


class Layout背景图排版(LayoutInit):
    def main(self):
        # shadow = Image.open(Path(__file__).parent / "img" / "背景图投影.png")
        spacing = 180
        bg = Image.new("RGBA", (self.xq_width, self.xq_height), (255, 255, 255, 255))
        left = 0
        for num, im in enumerate(self._pil_list):
            im = fun_图片裁剪(
                im=im, width=self.xq_width, height=self.xq_height, position="start"
            )

            bg.paste(im, (left, 0), im)
            left += spacing

            if num + 1 == 4:
                break

        # shadow_left = spacing - shadow.width
        # for x in range(3):
        #     bg.paste(shadow, (shadow_left, 0), shadow)
        #     shadow_left += spacing

        return bg
