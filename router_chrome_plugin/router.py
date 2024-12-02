from fastapi import APIRouter
from pydantic import BaseModel

from router_chrome_plugin.class_chrome_scrapy import ChromeScrapy
from router_chrome_plugin.class_make_tb_xq_str import MakeTaobaoXQStr

router = APIRouter(prefix="/chrome_plugin")
# ---------------- 传递HTML构建详情 ----------------


class XQReqModel(BaseModel):
    html: str


class XQResModel(BaseModel):
    xq_str: str


@router.post("/make_xq_str", response_model=XQResModel)
def fun_make_xq_str(item: XQReqModel) -> XQResModel:
    # html_file = Path(__file__).parent / "xq.html"
    # with open(html_file.as_posix(), encoding="utf-8", mode="w") as html:
    #     html.write(item.html)

    xq = MakeTaobaoXQStr(html=item.html)
    xq.main()

    return XQResModel(xq_str="success")


# ---------------- 传递HTML进行采集 ----------------


class ReqModel(BaseModel):
    shop_name: str
    material_site: str
    url: str
    html: str


class ResModel(BaseModel):
    msg: str


@router.post("/scrapy_material")
def fun_scrapy_material(item: ReqModel) -> ResModel:
    # html_file = Path(__file__).parent / "text.html"
    # with open(html_file.as_posix(), encoding="utf-8", mode="w") as html:
    #     html.write(item.html)

    chrome_scrapy = ChromeScrapy(
        shop_name=item.shop_name, material_site=item.material_site, html=item.html
    )
    res = chrome_scrapy.fun_insert_db()
    if res is True:
        return ResModel(msg="success")

    return ResModel(msg="faild")


# ---------------- 获取店铺名和素材网站 ----------------


class ShopNameModel(BaseModel):
    shop_name_list: list[str]
    material_site_list: list[str]


@router.get("/get_shop_name_material_site", response_model=ShopNameModel)
def fun_get_shop_name_material_site() -> ShopNameModel:
    return ShopNameModel(
        shop_name_list=["小夕素材", "饭桶设计", "泡泡素材", "松子素材"],
        material_site_list=[
            "千图",
            "包图",
            "摄图",
            "享设计",
            "青青草素材王国",
            "加油鸭素材铺",
            "漫语摄影",
            "三老爹",
            "T500",
            "猪大叔",
            "唐峰",
            "芒果",
            "巴扎嘿",
            "轨迹",
        ],
    )
