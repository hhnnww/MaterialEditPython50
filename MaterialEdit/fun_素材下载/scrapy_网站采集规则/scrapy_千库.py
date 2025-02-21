"""千库采集."""

from collections.abc import Generator

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def scrapy_千库(single_url: str, cookie: str) -> Generator[MaterialModel]:
    """千库采集."""
    html = fun_session(url=single_url, cookie=cookie)

    material_list = html.find(".data-box .fl")

    for obj in material_list:  # type: ignore  # noqa: PGH003
        center_box = obj.find(".center-box", first=True)
        if center_box is not None:
            url = "https:" + obj.find(".center-box", first=True).find(
                "a",
                first=True,
            ).attrs.get("href")
            img = "https:" + obj.find(".center-box a", first=True).find(
                "img",
                first=True,
            ).attrs.get("data-original")

            yield MaterialModel(url=url, img=img, state=False)
