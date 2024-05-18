import json
import re

import pyperclip
from fastapi import APIRouter
from pydantic import BaseModel
from requests_html import HTMLSession

from .fun_从百度网盘文件列表JSON中构建列表 import fun_构建网盘文件列表
from .fun_构建HEADER import fun_构建header

router = APIRouter()

# ---------------- 获取商家编码 ----------------


class GetMateialIdItem(BaseModel):
    material_name: str
    page_text: str


@router.post("/get_material_id")
def fun_获取商家编码(item_in: GetMateialIdItem) -> list[str]:
    """
    获取千牛和自动发货的商家编码
    千牛的商家编码可以删除仓库中的产品对应的网盘文件
    自动发货的商家编码可以用来获取网盘链接
    """
    return re.findall(rf"{item_in.material_name}(.*?)\r", item_in.page_text)


# ---------------- 删除网盘文件夹 ----------------


class DelBaiduFolder(BaseModel):
    maid_list: str
    header: str


@router.post("/del_baidu_folder")
def fun_删除网盘文件夹(item_in: DelBaiduFolder):
    """
    1 获取需要删除的产品的商家编码
    2 构建成百度网盘的路径
    3 发送请求删除这个路径
    """
    session = HTMLSession()
    # TODO 构建路径

    # 构建HEADER请求
    header = fun_构建header(header=item_in.header)

    # 发送请求
    for maid in item_in.maid_list:
        with session.post(
            url=item_in.header.split("\n")[0].split(" ")[1],
            data={"filelist": f"{maid}"},
            headers=header,
        ) as res:
            print(res.json())


# ---------------- 获取网盘分享链接 ----------------


class GetBaiduShareLinkItem(BaseModel):
    file_list_json: str  # 百度网盘请求中获取文件列表的JSON
    header: str  # 分享链接的原始HEADER
    maid_list: str  # 需要获取分享链接的商品ID列表


from .fun_获取自动发货中的商家编码 import fun_获取自动发货中的商家编码


@router.post("/get_baidu_share_link")
def fun_获取网盘分享链接(item_in: GetBaiduShareLinkItem):
    """
    获取网盘分享链接
    1 先从百度网盘的请求中返回的JSON获取文件夹ID
    2 获取分享文件夹的接口和HEADER
    3 从自动发货后台获取需要获取的产品ID
    """
    session = HTMLSession()

    # 从百度网盘请求中获取返回的JSON文件
    out_list = fun_构建网盘文件列表(res_json=item_in.file_list_json)

    # 构建HEADER请求
    header = fun_构建header(header=item_in.header)

    # 自动发货中的商家编码
    ma_id_list = fun_获取自动发货中的商家编码(item_in.maid_list)

    content_text = ""
    # 发出请求
    for ma_id in ma_id_list:
        fs_id = [item.id for item in out_list if item.filename == ma_id]

        if len(fs_id) > 0:
            with session.post(
                url=f'https://pan.baidu.com{item_in.header.split("\n")[0].split(" ")[1]}',
                data={
                    "period": 0,
                    "pwd": "8888",
                    "eflag_disable": True,
                    "channel_list": "[]",
                    "schannel": 4,
                    "fid_list": f"[{fs_id[0]}]",
                },
                headers=header,
            ) as res:
                res_json = res.json()
                share_link = f'{ma_id}\t"链接: {res_json.get("shorturl")}?pwd=8888"'
                print(share_link)
                content_text = content_text + share_link + "\n\n"

        else:
            print(f"{ma_id} 不存在")

    print(f"已经自动复制，可直接去粘贴。")
    pyperclip.copy(content_text)
