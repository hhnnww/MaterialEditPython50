"""爬虫基础信息."""

from requests_html import HTML


class ScrapyBase:
    def __init__(self, shop_name: str, material_site: str, html: str) -> None:
        """初始化爬虫基础信息.

        Args:
            shop_name (str): 店铺名
            material_site (str): 素材网站
            html (str): html代码

        """
        self.shop_name = shop_name
        self.material_site = material_site
        self.html = HTML(html=html)