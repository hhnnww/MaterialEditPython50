"""chrome插件来采集淘宝素材."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

from router_chrome_plugin.class_采集素材到数据库 import MaterialScrapyAction

router = APIRouter()


class ReqModel(BaseModel):
    """采集素材请求模型"""

    shop_name: str
    material_site: str
    url: str
    html: str


class ResModel(BaseModel):
    """采集素材返回模型"""

    msg: str


@router.post("/scrapy_material")
def fun_scrapy_material(item: ReqModel) -> ResModel:
    """开始采集素材路由."""
    logging.info(item)
    # html_file = Path(__file__).parent / "test.html"
    # html_file.write_text(item.html, encoding="utf-8")

    chrome_scrapy = MaterialScrapyAction(
        shop_name=item.shop_name,
        material_site=item.material_site,
        html=item.html,
    )
    res = chrome_scrapy.fun_insert_db()
    if res is True:
        return ResModel(msg="success")

    return ResModel(msg="faild")
