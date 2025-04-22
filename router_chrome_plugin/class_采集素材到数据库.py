"""素材爬取."""

import re
from collections.abc import Generator

from requests_html import Element

from MaterialEdit.fun_素材下载.fun_插入素材 import fun_插入素材
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.__class_new_tb import NewTbScrapy
from router_chrome_plugin.__class_old_tb import OldTbScrapy
from router_chrome_plugin.class_爬虫INIT import ScrapyBase


class MaterialScrapyAction(NewTbScrapy, OldTbScrapy, ScrapyBase):
    def fun_千库(self) -> Generator[MaterialModel]:
        """千库采集."""
        ma_list = self.html.find(
            selector="body > div.result-box.all.so > div.panel-box > div > "
            "div.clearfix.data-list.dataList.V-maronyV1.Vmarony.J_ViewCards."
            "marony-vertical > div.fl.marony-item",
            first=False,
        )
        for ma in ma_list:  # type: ignore  # noqa: PGH003
            url = "https:" + ma.find("a", first=True).attrs.get("href")
            img = "https:" + ma.find("img", first=True).attrs.get("data-original")
            yield MaterialModel(url=url, img=img, state=False)

    def fun_享设计(self) -> Generator[MaterialModel]:
        """享设计采集."""
        ma_list = self.html.find(r"#grid > li.item")
        for ma in ma_list:  # type: ignore  # noqa: PGH003
            img = ma.find("a img", first=True).attrs.get("src")
            img = re.sub(r"\?x-oss-process.*", "", img)

            url = ma.find("a", first=True).attrs.get("href")
            url = re.sub(r"\?inviteCode=.*", "", url)
            url = url.replace("http://img.img5.com.cn", "https://www.design006.com")

            yield MaterialModel(
                url=url,
                img=img,
                state=False,
            )

    def fun_freepik(self) -> Generator[MaterialModel]:
        """freepik采集."""
        url, img = "", ""
        ma_list = self.html.find("figure")
        if ma_list is not None and isinstance(ma_list, list):
            for ma in ma_list:
                find = ma.find("a", first=True)
                if find is not None and isinstance(find, Element):
                    url = find.attrs.get("href", "")

                find = ma.find("img", first=True)
                if find is not None and isinstance(find, Element):
                    img = find.attrs.get("src", "")

                yield MaterialModel(url=url, img=img, state=False)

    def fun_insert_db(self) -> bool:
        """插入到数据库."""
        state = False
        ma_list = []
        if self.material_site in [
            "三老爹",
            "加油鸭素材铺",
            "漫语摄影",
            "轨迹",
            "巴扎嘿",
            "唐峰",
        ]:
            ma_list = self.fun_get_new_tb()
        elif self.material_site in ["青青草素材王国"]:
            ma_list = self.fun_get_old_tb()
        elif self.material_site == "千库":
            ma_list = self.fun_千库()
        elif self.material_site == "享设计":
            ma_list = self.fun_享设计()
        elif self.material_site == "freepik":
            ma_list = self.fun_freepik()

        for obj in ma_list:
            fun_插入素材(
                shop_name=self.shop_name,
                material_site=self.material_site,
                material_model=obj,
            )
            state = True

        return state
