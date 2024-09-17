import os
import re

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/open_baidu_link")


class ItemIn(BaseModel):
    md_text: str


@router.post("/open_link")
def open_baidu_link(item_in: ItemIn):
    text = item_in.md_text
    link_list = re.findall(r"(https://pan.baidu.com.*?)\n", text)
    for link in link_list:
        link: str
        link = re.sub(r"\s", "", link)

        if "提取码" in link:
            link = re.sub("提取码:.*", "", link)

        if "?pwd" not in link:
            tqm: str = re.findall(rf"{link}[\s\S]*?提取码：(.*?)\n", text)[0]
            tqm = re.sub(r"\s", "", tqm)
            link = f"{link}?pwd={tqm}"

        os.startfile(link)
