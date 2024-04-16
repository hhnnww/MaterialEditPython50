from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_包图(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    material_element_list = html.find(
        r"body > div.page-body.skin-wrap.body-background-gradient > div.bt-body.search.clearfix > "
        r"div.search-list.box-bg-search.box-bottom-gradient.clearfix > dl"
    )

    for obj in material_element_list:
        if "searchAdver" not in obj.attrs.get("class"):
            url = "https:" + obj.find("a.jump-details", first=True).attrs.get("href")

            img_element = obj.find("a.jump-details img", first=True)
            if img_element is None:
                return

            img_url = "https:" + img_element.attrs.get("data-url")

            yield MaterialModel(url=url, img=img_url, state=False)
