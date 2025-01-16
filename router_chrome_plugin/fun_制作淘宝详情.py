"""构建淘宝详情"""

import re

import pyperclip
from pydantic import BaseModel
from requests_html import HTML


class ImageModel(BaseModel):
    """图像模型"""

    name: str
    name_number: int
    img: str


class MakeTaobaoXQStr:
    """制作淘宝详情"""

    def __init__(self, html: str) -> None:
        """制作淘宝详情的代码.

        传入淘宝后台的图片列表页面的HTML代码.
        使用HTML类来解析HTML代码.
        构建所有的图片列表.

        Args:
            html (str): 图片列表页面的原始HTML代码

        """
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
                    ImageModel(name=name, name_number=name_int, img=img)
                )
                max_num = max([obj.name_number for obj in self.image_mode_list])
                if len(self.image_mode_list) == max_num:
                    break

        self.image_mode_list.sort(key=lambda k: k.name_number)

        html = ""
        for img_mode in self.image_mode_list:
            html += f"<img src={img_mode.img} />"

        pyperclip.copy(html)
