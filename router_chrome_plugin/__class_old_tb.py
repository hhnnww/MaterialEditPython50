from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.__class_scrapy_init import ScrapyInit


class OldTbScrapy(ScrapyInit):
    def fun_get_old_tb(self):
        ma_list = self.html.find(
            "#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div > dl"
        )
        for ma in ma_list:  # type: ignore
            link = "https:" + ma.find("a", first=True).attrs.get("href")
            img = "https:" + ma.find("img", first=True).attrs.get("src")
            yield MaterialModel(url=link, img=img, state=False)
