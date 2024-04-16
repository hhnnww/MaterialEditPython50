from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_千图(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(r"div.qtd-card")

    for obj in material_list:
        url = "https:" + obj.find("a", first=True).attrs.get("href")
        img = "https:" + obj.find("a img", first=True).attrs.get("data-original")

        yield MaterialModel(url=url, img=img, state=False)
