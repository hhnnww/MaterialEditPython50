"""千图网站采集规则"""

from collections.abc import Generator
from typing import Any

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_千图(single_url: str, cookie: str) -> Generator[MaterialModel, Any, None]:
    """千图网站采集规则."""
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find("div.qtd-card")
    url, img = "", ""
    if isinstance(material_list, list):
        for obj in material_list:
            find = obj.find("a", first=True)
            if isinstance(find, Element):
                url = "https:" + find.attrs.get("href", "")

            find = obj.find("a img", first=True)
            if isinstance(find, Element):
                img = "https:" + find.attrs.get("data-original", "")

            yield MaterialModel(url=url, img=img, state=False)
