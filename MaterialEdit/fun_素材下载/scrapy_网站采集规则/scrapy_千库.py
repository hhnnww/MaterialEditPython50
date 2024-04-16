from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_千库(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(r".data-box .data-list .fl")

    for obj in material_list:
        url = "https:" + obj.find("a.img-box", first=True).attrs.get("href")
        img = "https:" + obj.find("a.img-box img.lazy", first=True).attrs.get("data-original")

        yield MaterialModel(url=url, img=img, state=False)
