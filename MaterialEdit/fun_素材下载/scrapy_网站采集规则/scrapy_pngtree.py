"""pngtree."""

from collections.abc import Generator
from typing import Any

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_pngtree(single_url: str, cookie: str) -> Generator[MaterialModel, Any, None]:
    """爬取pngtree网站."""
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find("section div ul li")
    url, img = "", ""
    if material_list is not None and isinstance(material_list, list):
        for obj in material_list:
            find = obj.find("a", first=True)
            if isinstance(find, Element):
                url = "https:" + find.attrs.get("href", "")

            find = obj.find("img", first=True)
            if isinstance(find, Element):
                if find.attrs.get("data-src"):
                    img = "https:" + find.attrs.get("data-src", "")
                else:
                    img = find.attrs.get("src", "")

        yield MaterialModel(url=url, img=img, state=False)
