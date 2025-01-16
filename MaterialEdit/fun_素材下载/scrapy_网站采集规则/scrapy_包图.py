"""scraping materials from a specified URL."""

from collections.abc import Generator
from typing import Any

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_包图(single_url: str, cookie: str) -> Generator[MaterialModel, Any, None]:
    """包图采集."""
    html = fun_session(url=single_url, cookie=cookie)

    material_element_list = html.find(
        "body > div.page-body.skin-wrap.body-background-gradient > "
        "div.bt-body.search.clearfix.search-main > div.search-list.w-search-list."
        "box-bottom-gradient.clearfix > div.result-list.media-list > div > dl > dt",
    )
    if material_element_list is not None and isinstance(material_element_list, list):
        for obj in material_element_list:
            find = obj.find("a.jump-details", first=True)
            if isinstance(find, Element):
                url = "https:" + find.attrs.get("href", "")

            find = obj.find("a.jump-details img", first=True)
            if isinstance(find, Element):
                data_url = find.attrs.get("data-url")
                if data_url is None:
                    data_url = find.attrs.get("src", "")

                img_url = "https:" + data_url

            yield MaterialModel(url=url, img=img_url, state=False)
