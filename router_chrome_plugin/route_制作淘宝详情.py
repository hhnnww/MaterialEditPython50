"""根据图片页面的HTML构建图片列表."""

from fastapi import APIRouter
from pydantic import BaseModel

from router_chrome_plugin.fun_制作淘宝详情 import MakeTaobaoXQStr

router = APIRouter()


class XQReqModel(BaseModel):
    """请求模型"""

    html: str


class XQResModel(BaseModel):
    """返回模型"""

    xq_str: str


@router.post("/make_xq_str")
def fun_make_xq_str(item: XQReqModel) -> XQResModel:
    """制作淘宝详情"""
    xq = MakeTaobaoXQStr(html=item.html)
    xq.main()

    return XQResModel(xq_str="success")
