from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_千库(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(r".data-list div.fl.marony-item")

    for obj in material_list:  # type: ignore
        url = "https:" + obj.find("a.img-box", first=True).attrs.get("href")
        img = "https:" + obj.find("a.img-box img", first=True).attrs.get(
            "data-original"
        )

        yield MaterialModel(url=url, img=img, state=False)
