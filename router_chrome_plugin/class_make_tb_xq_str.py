import re

import pyperclip
from pydantic import BaseModel
from requests_html import HTML, Element


class ImageModel(BaseModel):
    name: str
    name_number: int
    img: str


class MakeTaobaoXQStr:
    def __init__(self, html: str, shop_name: str) -> None:
        self.html_obj = HTML(html=html)

        self.image_mode_list = []
        self.shop_name = shop_name

    def main(self):
        for obj in self.html_obj.find(".item"):  # type: ignore
            obj: Element
            name = obj.find(".name", first=True).text  # type: ignore

            max_num = 0
            if "xq_" in name:
                name_int = int("".join(re.findall(r"\d", name)))
                img: str = (
                    obj.find("img", first=True).attrs.get("src").replace("_100x100", "")  # type: ignore
                )

                self.image_mode_list.append(
                    ImageModel(name=name, name_number=name_int, img=img)
                )
                max_num = max([obj.name_number for obj in self.image_mode_list])

                if len(self.image_mode_list) == max_num:
                    break

            # if "st_1" in name:
            #     break

        self.image_mode_list.sort(key=lambda k: k.name_number)

        html = ""

        if self.shop_name == "小夕素材":
            html += """<div class="dm_module" data-id="11286177" data-title="会员免费" id="ids-module-11286177"><p><a href="https://item.taobao.com/item.htm?id=669741402774" target="_blank"><img src="https://img.alicdn.com/imgextra/i3/862322326/O1CN01UvKI1q1T3MFrkak0p_!!862322326.jpg" /></a></p></div>"""
            for img_mode in self.image_mode_list:
                html += f"<img src={img_mode.img} />"
            html += """<div class="dm_module" data-id="11715980" data-title="查看更多" id="ids-module-11715980"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/862322326/O1CN010xoYI01T3MFkXBXaM_!!862322326.jpg" style="max-width: 750.0px;" /></p></div><p>&nbsp;</p>"""

        elif self.shop_name == "松子素材":
            html += """<div class="dm_module" data-id="12332582" data-title="店铺VIP" id="ids-module-12332582"><p><a href="https://item.taobao.com/item.htm?ft=t&amp;id=855196889014" target="_blank"><img align="absmiddle" data-spm-anchor-id="a2126o.11854294.0.i1.1b064831nYCTxO" src="https://img.alicdn.com/imgextra/i2/2218686144077/O1CN01GdnmRz1fzJlufJhRl_!!2218686144077.jpg" style="max-width:750px;" /></a></p></div>"""
            for img_mode in self.image_mode_list:
                html += f"<img src={img_mode.img} />"
            html += """<div class="dm_module" data-id="12332581" data-title="阅读更多" id="ids-module-12332581"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/2218686144077/O1CN01wvhDph1fzJlufZg7J_!!2218686144077.jpg" style="max-width:750px;" /></p></div>"""

        elif self.shop_name == "饭桶设计":
            for img_mode in self.image_mode_list:
                html += f"<img src={img_mode.img} />"

        elif self.shop_name == "泡泡素材":
            html += """<div class="dm_module" data-id="12230360" data-title="加入会员" id="ids-module-12230360"><p><a href="https://item.taobao.com/item.htm?id=835832878257" target="_blank"><img align="absmiddle" data-spm-anchor-id="a2126o.11854294.0.i3.76a94831YIlfLs" src="https://img.alicdn.com/imgextra/i2/2214924450004/O1CN01XEcSKj1BtsaGLhttT_!!2214924450004.jpg" style="max-width:750px;" /></a></p></div>"""
            for img_mode in self.image_mode_list:
                html += f"<img src={img_mode.img} />"
            html += """<div class="dm_module" data-id="12230361" data-title="查看更多" id="ids-module-12230361"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/2214924450004/O1CN012kZUT81BtsaHKig8v_!!2214924450004.jpg" style="max-width:750px;" /></p></div>"""

        pyperclip.copy(html)
