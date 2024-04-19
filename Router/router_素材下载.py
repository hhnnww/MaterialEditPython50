from pathlib import Path

from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from tqdm import tqdm

from MaterialEdit.fun_素材下载 import (
    fun_envato_图片下载,
    fun_插入素材,
    fun_获取素材,
    fun_获取集合,
    fun_采集,
)

router = APIRouter(prefix="/MaterialDown")


class MaterialDownModel(BaseModel):
    shop_name: str
    material_site: str
    down_path: str

    scrapy_url: str
    scrapy_num: int
    cookie: str

    page: int


# ---------------- 文件夹合并 ----------------


@router.post("/down_path_merge")
def fun_down_path_merge(item: MaterialDownModel):
    down_path = Path(item.down_path)

    # 确定新文件夹
    num = 1
    new_path = down_path / f"新建文件夹"
    while new_path.exists() is True:
        num += 1
        new_path = down_path / f"新建文件夹({num})"

    for in_file in tqdm(list(down_path.iterdir()), ncols=100, desc="移动到新建文件夹"):
        if "新建文件夹" not in in_file.stem:
            if new_path.exists() is False:
                new_path.mkdir()

            in_file_new_path = new_path / in_file.name

            num = 1
            while in_file_new_path.exists() is True:
                in_file_new_path = in_file_new_path.with_stem(
                    f"{in_file_new_path.stem}_({num})"
                )
                num += 1

            in_file.rename(in_file_new_path)


# ---------------- 截止素材 ----------------


class CutMaterialModel(BaseModel):
    shop_name: str
    material_site: str
    material_id: str


@router.post("/cut_material_list")
def cut_material_list(item: CutMaterialModel):
    collect = fun_获取集合(shop_name=item.shop_name, material_site=item.material_site)
    cut_obj = collect.find_one({"_id": ObjectId(item.material_id)})
    collect.delete_many({"create_date": {"$lte": cut_obj.get("create_date")}})

    return "ok"


# ---------------- 采集素材 ----------------


@router.post("/scrapy_material")
def scrapy_material(item: MaterialDownModel):
    for obj in fun_采集(
        base_url=item.scrapy_url,
        material_site=item.material_site,
        cookie=item.cookie,
        num=item.scrapy_num,
    ):
        fun_插入素材(
            shop_name=item.shop_name,
            material_site=item.material_site,
            material_model=obj,
        )


# ---------------- 清空未下载素材 ----------------


@router.post("/clear_un_down_material")
def clear_un_down_material(item: MaterialDownModel):
    collect = fun_获取集合(shop_name=item.shop_name, material_site=item.material_site)
    collect.delete_many({"state": False})
    return "ok"


# ---------------- 单个素材下载跳转 ----------------


@router.get("/get_material_down_link")
def get_material_down_link(
    shop_name: str, material_site: str, material_id: str, down_path: str
):
    collect = fun_获取集合(shop_name=shop_name, material_site=material_site)
    obj = collect.find_one({"_id": ObjectId(oid=material_id)})

    if material_site == "envato":
        fun_envato_图片下载(obj, down_path)

    collect.update_one(obj, {"$set": {"state": True}})
    return RedirectResponse(url=obj.get("url"), status_code=301)


# ---------------- 获取素材列表 ----------------


@router.post("/get_material_list")
def get_material_list(item: MaterialDownModel):
    res = fun_获取素材(
        shop_name=item.shop_name, material_site=item.material_site, page=item.page
    )
    ma_list = list(res[0])
    return dict(material_list=ma_list, count=res[1])
