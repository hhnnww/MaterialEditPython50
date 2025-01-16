"""摄图网采集."""

import logging
from collections.abc import Generator
from typing import Any

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_摄图(single_url: str, cookie: str) -> Generator[MaterialModel, Any, None]:
    """采集摄图网."""
    logging.info(single_url)
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(
        selector="#wrapper > div > div.imgshow.clearfix > div > div",
    )
    if isinstance(material_list, list):
        for obj in material_list:
            if "ad_type" in obj.attrs.get("class", ""):
                continue

            find = obj.find("a", first=True)
            if find is not None and isinstance(find, Element):
                url = next(iter(find.absolute_links))

            find = obj.find("a img", first=True)
            if find is not None and isinstance(find, Element):
                img = find.attrs.get("data-original")
                if img is None:
                    img = find.attrs.get("src", "")

            yield MaterialModel(url=url, img="https:" + img, state=False)
