"""新版本淘宝列表页采集."""

from collections.abc import Generator
from typing import TYPE_CHECKING

from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel
from router_chrome_plugin.class_爬虫INIT import ScrapyBase

if TYPE_CHECKING:
    from requests_html import Element


class NewTbScrapy(ScrapyBase):
    def fun_get_new_tb(self) -> Generator[MaterialModel]:
        """采集新版本的淘宝页面."""
        ma_list = self.html.find(
            "#ice-container > div > div > div.container--ZphYH1vW > div:nth-child(3) > div > div",  # noqa: E501
        )  # type: ignore  # noqa: PGH003
        for ma in ma_list:  # type: ignore  # noqa: PGH003
            link_find: Element = ma.find("a", first=True)

            if link_find is not None:
                link = next(iter(link_find.absolute_links))
                img_find: Element = ma.find("img", first=True)
                img = img_find.attrs.get("src")

                if isinstance(img, str) and ".png" not in img:
                    yield MaterialModel(url=link, img=img, state=False)
