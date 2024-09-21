from PIL import Image

from MaterialEdit.fun_图片编辑 import (
    fun_单行文字转图片,
    fun_单行文字转图片2,
    fun_图片竖向拼接,
    fun_画一个圆形横框,
    fun_画一个圆角矩形,
    fun_获取单个水印,
)

from .class_style_init import StyleInit


class Style黑鲸笔刷(StyleInit):
    margin = 40
    font_size = 40

    def fun_标题(self) -> Image.Image:
        return fun_单行文字转图片(
            text=self.title,
            chinese_font_name="opposans",
            english_font_name="montserrat",
            font_weight="bold",
            font_size=100,
            fill_color=(255, 255, 255, 255),
            background_color=(0, 0, 0, 255),
        )

    def fun_LOGO(self) -> Image.Image:
        logo = fun_获取单个水印(80, fill_clor=(255, 255, 255, 255))
        logo_bg = fun_画一个圆角矩形(
            width=logo.width + 40,
            height=int((logo.height + 40) * 2),
            border_radius=60,
            fill_color=(0, 0, 0, 255),
        )
        logo_bg = logo_bg.crop(
            (0, int(logo_bg.height / 2), logo_bg.width, logo_bg.height)
        )
        logo_bg.paste(logo, (20, 15), logo)

        return logo_bg

    def fun_素材ID(self) -> Image.Image:
        material_id_pil = fun_单行文字转图片2(
            text="ID:" + self.material_id,
            font_weight="heavy",
            size=20,
            fill=(255, 255, 255, 255),
            background=(0, 0, 0, 255),
        )

        material_id_bg = fun_画一个圆形横框(
            material_id_pil.width + 40,
            material_id_pil.height + 20,
            (0, 0, 0, 255),
            (255, 255, 255, 0),
        )

        material_id_bg.paste(material_id_pil, (20, 10), material_id_pil)

        return material_id_bg

    def fun_广告语(self) -> Image.Image:
        ad_title_pil = fun_单行文字转图片2(
            text=f"{self.shop_name}/海外精品资源",
            size=self.font_size,
            fill=(255, 255, 255, 255),
            background=(0, 0, 0, 255),
            font_weight="normal",
        )
        return ad_title_pil

    def fun_格式标题(self) -> Image.Image:
        return fun_单行文字转图片2(
            text=f"{self.format_title}",
            size=self.font_size,
            fill=(255, 255, 255, 255),
            background=(0, 0, 0, 255),
            font_weight="normal",
        )

    def main(self):
        bottom_bg = Image.new("RGBA", (1500, 500), (0, 0, 0, 255))
        # bottom_bg = fun_画一个圆角矩形(
        #     1500, 1000, 80, (0, 0, 0, 255), (255, 255, 255, 255)
        # )
        # bottom_bg = bottom_bg.crop((0, 500, bottom_bg.width, bottom_bg.height))

        # 广告语
        ad_pil = self.fun_广告语()
        bottom_bg.paste(ad_pil, (self.margin, self.margin), ad_pil)

        # 右边的格式标题
        format_pil = self.fun_格式标题()
        bottom_bg.paste(
            format_pil,
            (bottom_bg.width - format_pil.width - self.margin, self.margin),
            format_pil,
        )

        # 标题
        title_pil = self.fun_标题()
        bottom_bg.paste(
            title_pil,
            (
                self.margin,
                int(
                    (
                        bottom_bg.height
                        - self.margin
                        - format_pil.height
                        - title_pil.height
                    )
                    / 2
                    + (format_pil.height + self.margin)
                ),
            ),
            title_pil,
        )

        bg = fun_图片竖向拼接(
            image_list=[self.bg, bottom_bg],
            spacing=0,
            align_item="center",
            background_color=(0, 0, 0, 255),
        )

        logo_pil = self.fun_LOGO()
        bg.paste(logo_pil, (60, 0), logo_pil)

        material_id_pil = self.fun_素材ID()
        bg.paste(
            material_id_pil,
            (bg.width - material_id_pil.width - 30, 30),
            material_id_pil,
        )

        return bg
