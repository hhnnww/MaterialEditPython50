from ..fun_session import fun_session
from ..model_素材格式 import MaterialModel


def scrapy_摄图(single_url: str, cookie: str):
    print(single_url)
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(r"#wrapper > div > div.imgshow.clearfix > div > div")

    for obj in material_list:
        if "ad_type" in obj.attrs.get("class"):
            continue

        url = list(obj.find("a", first=True).absolute_links)[0]

        img_element = obj.find("a img", first=True)
        img = img_element.attrs.get("data-original")
        if img is None:
            img = img_element.attrs.get("src")

        yield MaterialModel(url=url, img="https:" + img, state=False)
