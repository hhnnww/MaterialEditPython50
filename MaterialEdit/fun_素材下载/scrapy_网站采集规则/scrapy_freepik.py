"""freepik scrapy."""

from collections.abc import Generator

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_freepik(single_url: str, cookie: str) -> Generator[MaterialModel]:
    """根据提供的单个URL和cookie从Freepik网站抓取素材信息。

    参数:
        single_url (str): 目标网页的URL。
        cookie (str): 用于访问目标网页的cookie。
    返回:
        generator: 生成包含素材信息的MaterialModel对象,包括素材的URL、图片链接和状态。
    """
    html = fun_session(url=single_url, cookie=cookie)
    material_list = html.find("figure", first=False)
    url, img = "", ""
    if material_list is not None:
        if not isinstance(material_list, list):
            material_list = [material_list]

        for obj in material_list:
            find = obj.find("a", first=True)
            if isinstance(find, Element):
                url = find.attrs.get("href", "")

            find = obj.find("a img", first=True)
            if isinstance(find, Element):
                img = find.attrs.get("data-src", "")

            yield MaterialModel(url=url, img=img, state=False)


if __name__ == "__main__":
    url = "https://www.freepik.com/search?author=21513339&format=author&last_filter=page&last_value=3&page=3&sort=recent#uuid=2e1b27ba-93c1-4358-af59-c4414c20224d"
    cookie = """_cs_c=0; _hjSessionUser_1331604=eyJpZCI6ImU0NzU2NDVhLTM3NTAtNTliMy05YjY3LTY0ZmY0MzM5NWY1ZiIsImNyZWF0ZWQiOjE3MjcwODE3OTE0ODksImV4aXN0aW5nIjp0cnVlfQ==; new_regular_detail_test=B; TUNES_IN_VIDEO=0; GENERATE_SIMILAR_VIDEO=0; _gcl_au=1.1.640379980.1736998979; premiumQueue=D; _ga=GA1.1.1254794049.1736998979; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jan+16+2025+11%3A43%3A13+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=34c3b134-7c33-45fd-a409-694d54243afd&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0005%3A0&AwaitingReconsent=false; _ga_QWX66025LC=GS1.1.1736998979.1.1.1736998994.45.0.0; RT="z=1&dm=www.freepik.com&si=e3f4ebb7-52a5-4100-b2c1-42e16b695099&ss=m5yscbfs&sl=2&tt=665&rl=1&nu=1atiewrza&cl=j11&obo=1&ld=3fof&r=7qfiakfv&ul=3fof"""
    for material in scrapy_freepik(url, cookie):
        print(material)
