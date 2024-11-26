from requests_html import HTML


class ScrapyInit:
    def __init__(self, shop_name: str, material_site: str, html: str) -> None:
        self.shop_name = shop_name
        self.material_site = material_site
        self.html = HTML(html=html)
