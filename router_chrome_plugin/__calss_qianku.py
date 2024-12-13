from requests_html import Element

from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.__class_scrapy_init import ScrapyInit


class Qianku(ScrapyInit):
    def fun_get_qianku(self):
        ma_list = self.html.find(
            "body > div.result-box.all.so > div.panel-box > div > div.clearfix.data-list.dataList.V-maronyV1.Vmarony.J_ViewCards.marony-vertical > div.fl.marony-item"
        )

        for ma in ma_list:  # type: ignore
            ma: Element
            url = "https:" + ma.find("a", first=True).attrs.get("href")  # type: ignore
            img = "https:" + ma.find("img", first=True).attrs.get("data-original")  # type: ignore
            yield MaterialModel(url=url, img=img, state=False)
