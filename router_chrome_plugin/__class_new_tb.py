from requests_html import Element

from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.__class_scrapy_init import ScrapyInit


class NewTbScrapy(ScrapyInit):
    def fun_get_new_tb(self):
        ma_list = self.html.find(
            "#ice-container > div > div > div.flexCell--O42zbLr4 > div.shopProductShelfArea--Z6GzvxkU > div > div:nth-child(3) > div > div.cardContainer--CwazTl0O"
        )
        for ma in ma_list:  # type: ignore
            link_find: Element = ma.find("a", first=True)
            link = list(link_find.absolute_links)[0]

            img_find: Element = ma.find("img", first=True)
            img = img_find.attrs.get("src")

            if isinstance(img, str) and ".png" not in img:
                yield MaterialModel(url=link, img=img, state=False)
