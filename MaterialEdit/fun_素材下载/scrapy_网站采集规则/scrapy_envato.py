from pprint import pprint

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def fun_获取图片(img_dict: dict, reverse: bool = True):
    size_list = [
        "w2740",
        "w2038",
        "w1370",
        "w1170",
        "w1019",
        "w900",
        "w710",
        "w632",
        "w433",
    ]

    if reverse is not True:
        size_list.reverse()

    for obj in size_list:
        if img_dict.get(obj) is not None:
            return img_dict.get(obj)
    return None


def scrapy_envato(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)
    objs = html.find("nav>div")
    pprint(objs)
    for obj in objs:
        pprint(obj, "fuck")
        url, img, name, all_list = "", "", "", []
        yield MaterialModel(
            url=url,
            img=img,
            name=name,
            img_list=all_list,
            state=False,
        )
