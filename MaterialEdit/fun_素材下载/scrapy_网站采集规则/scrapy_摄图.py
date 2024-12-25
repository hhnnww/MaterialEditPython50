"""摄图网采集."""

import logging
from collections.abc import Generator
from typing import Any

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_摄图(single_url: str, cookie: str) -> Generator[MaterialModel, Any, None]:
    """采集摄图网."""
    logging.info(single_url)
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(selector=r"#wrapper > div > div.imgshow.clearfix > div > div")

    for obj in material_list:
        if "ad_type" in obj.attrs.get("class"):
            continue

        url = next(iter(obj.find("a", first=True).absolute_links))

        img_element = obj.find("a img", first=True)
        img = img_element.attrs.get("data-original")
        if img is None:
            img = img_element.attrs.get("src")

        yield MaterialModel(url=url, img="https:" + img, state=False)
