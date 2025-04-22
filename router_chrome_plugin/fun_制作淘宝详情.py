"""构建淘宝详情"""

import re

import pyperclip
from pydantic import BaseModel
from requests_html import HTML, Element


class ImageModel(BaseModel):
    """图像模型"""

    name: str
    name_number: int
    img: str


class MakeTaobaoXQStr:
    """制作淘宝详情"""

    def __init__(self, html: str) -> None:
        """制作淘宝详情的代码."""
        self.html_obj = HTML(html=html)
        self.image_mode_list: list[ImageModel] = []

    def main(self) -> None:
        """开始制作淘宝详情"""
        for obj in self.html_obj.find(".item"):  # type: ignore  # noqa: PGH003
            name = obj.find(".name", first=True).text  # type: ignore  # noqa: PGH003

            max_num = 0
            if "xq_" in name:
                name_int = int("".join(re.findall(r"\d", name)))
                img = (
                    obj.find("img", first=True).attrs.get("src").replace("_100x100", "")
                )
                self.image_mode_list.append(
                    ImageModel(name=name, name_number=name_int, img=img),
                )
                max_num = max([obj.name_number for obj in self.image_mode_list])
                if len(self.image_mode_list) == max_num:
                    break
        self.image_mode_list.sort(key=lambda k: k.name_number)

        html = ""
        vip_free = ""
        read_more = ""

        sidebar_ele = self.html_obj.find(
            "#container > div > div.hasEms.container > div.main > div > "
            "div.opt-body > div.cates > div > div",
            first=True,
        )

        if isinstance(sidebar_ele, Element):
            if "小夕素材" in sidebar_ele.text:
                vip_free = (
                    '<div class="dm_module" data-id="11286177" data-title="会'
                    '员免费" id="ids-module-11286177"><p><a data-spm-anchor-id="a2126o'
                    '.11854294.0.0" href="https://item.taobao.com/item.htm?id=66974140'
                    '2774" target="_blank"><img data-spm-anchor-id="a2126o.11854294.0.'
                    'i4.39c14831lYQ9jY" src="https://img.alicdn.com/imgextra/i4/86232232'
                    '6/O1CN010fYimm1T3MGpxFKsf_!!862322326.png" /></a></p></div>'
                )

                read_more = (
                    '<div class="dm_module" data-id="11715980" data-title="查看更多'
                    '" id="ids-module-11715980"><p><img align="absmiddle" src="https://img.'
                    "alicdn.com/imgextra/i1/862322326/O1CN0186snmc1T3MGobZ9lu_!!862322326.p"
                    'ng" style="max-width:750px;" /></p></div>'
                )
            elif "饭桶设计" in sidebar_ele.text:
                vip_free = (
                    '<div class="dm_module" data-id="11852755" data-title="会员免费" '
                    'id="ids-module-11852755"><p><a data-spm-anchor-id="a213gs.2603'
                    '7848.0.0" href='
                    '"https://item.taobao.com/item.htm?id=863734583285" target="_'
                    'blank"><img align="a'
                    'bsmiddle" data-spm-anchor-id="a213gs.26037848.0.i4.75c84831'
                    'wyhJxl" src="https://im'
                    "g.alicdn.com/imgextra/i2/389353239/O1CN01y8Rksy1ZnVsWvrW5"
                    'g_!!389353239.png" /></a></p>'
                    "</div>"
                )
                read_more = (
                    '<div class="dm_module" data-id="12065804" '
                    'data-title="查看更多" id="ids-module-12065804"><p><img '
                    'align="absmiddle" src="https://img.alicdn.com/imgextra/i2'
                    '/389353239/O1CN01j95yV41ZnVsUjnCVS_!!389353239.png" /></p>'
                    "</div>"
                )

        html += vip_free

        for img_mode in self.image_mode_list:
            html += f"<img src={img_mode.img} />"

        html += read_more
        pyperclip.copy(html)
