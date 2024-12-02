import re

import pyperclip
from pydantic import BaseModel
from requests_html import HTML, Element


class ImageModel(BaseModel):
    name: str
    name_number: int
    img: str


class MakeTaobaoXQStr:
    def __init__(self, html: str) -> None:
        self.html_obj = HTML(html=html)
        self.image_mode_list = []

    def main(self):
        for obj in self.html_obj.find(".item"):  # type: ignore
            obj: Element
            name = obj.find(".name", first=True).text  # type: ignore
            if "xq_" in name:
                name_int = int("".join(re.findall(r"\d", name)))
                img: str = (
                    obj.find("img", first=True).attrs.get("src").replace("_100x100", "")  # type: ignore
                )

                self.image_mode_list.append(
                    ImageModel(name=name, name_number=name_int, img=img)
                )

            if "st_1" in name:
                break

        self.image_mode_list.sort(key=lambda k: k.name_number)

        html = """<div class="dm_module" data-id="11286177" data-title="会员免费" id="ids-module-11286177"><p><a href="https://item.taobao.com/item.htm?id=669741402774" target="_blank"><img src="https://img.alicdn.com/imgextra/i3/862322326/O1CN01UvKI1q1T3MFrkak0p_!!862322326.jpg" /></a></p></div>"""

        for img_mode in self.image_mode_list:
            html += f"<img src={img_mode.img} />"

        html += """<div class="dm_module" data-id="11715980" data-title="查看更多" id="ids-module-11715980"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/862322326/O1CN010xoYI01T3MFkXBXaM_!!862322326.jpg" style="max-width: 750.0px;" /></p></div><p>&nbsp;</p>"""

        pyperclip.copy(html)
