"""享设计采集"""

import json
import logging
from collections.abc import Generator

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_享设计(single_url: str, cookie: str) -> Generator[MaterialModel, None]:
    """享设计采集"""
    html = fun_session(url=single_url, cookie=cookie)
    raw_json = json.loads(html.html)

    res_list = raw_json.get("result")

    if res_list is not None:
        for obj in res_list:
            img = "https://imgs.design006.com/" + obj.get("preview_image")
            url = (
                "https://www.design006.com/detail-"
                + obj.get("prefix_id")
                + obj.get("id")
            )
            logging.info(msg={img, url})
            yield MaterialModel(url=url, img=img, state=False)
