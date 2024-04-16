from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_pngtree(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find("section div ul li")

    for obj in material_list:
        url = "https:" + obj.find("a", first=True).attrs.get("href")
        img = obj.find("a img", first=True).attrs.get("data-src")

        if img is None:
            img = obj.find("a img", first=True).attrs.get("src")

        yield MaterialModel(url=url, img=img, state=False)
