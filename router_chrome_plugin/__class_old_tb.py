from collections.abc import Generator

from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.class_爬虫INIT import ScrapyBase


class OldTbScrapy(ScrapyBase):
    def fun_get_old_tb(self) -> Generator[MaterialModel]:
        """采集老版本淘宝页面."""
        ma_list = self.html.find(
            "#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div > dl",
        )
        for ma in ma_list:  # type: ignore  # noqa: PGH003
            link = "https:" + ma.find("a", first=True).attrs.get("href")
            img = "https:" + ma.find("img", first=True).attrs.get("src")
            yield MaterialModel(url=link, img=img, state=False)
