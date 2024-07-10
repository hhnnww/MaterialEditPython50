from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_包图(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_element_list = html.find(
        "body > div.page-body.skin-wrap.body-background-gradient > div.bt-body.search.clearfix.search-main > div.search-list.w-search-list.box-bottom-gradient.clearfix > div.result-list.media-list > div > dl > dt"
    )

    for obj in material_element_list:
        url = "https:" + obj.find("a.jump-details", first=True).attrs.get("href")

        img_element = obj.find("a.jump-details img", first=True)
        if img_element is None:
            return

        data_url = img_element.attrs.get("data-url")
        if data_url is None:
            data_url = img_element.attrs.get("src")

        img_url = "https:" + data_url

        yield MaterialModel(url=url, img=img_url, state=False)
