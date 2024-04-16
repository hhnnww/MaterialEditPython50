from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel
import json


def scrapy_享设计(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)
    raw_json: dict = json.loads(html.html)

    for obj in raw_json.get("result"):
        img = "https://imgs.design006.com/" + obj.get("preview_image")
        url = "https://www.design006.com/detail-" + obj.get("prefix_id") + obj.get("id")

        yield MaterialModel(url=url, img=img, state=False)
