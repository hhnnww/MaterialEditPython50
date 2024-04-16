import os
import re

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/open_baidu_link")


class ItemIn(BaseModel):
    md_text: str


@router.post("/open_link")
def open_baidu_link(item_in: ItemIn):
    down_link_list = []
    for t in item_in.md_text.split("\n\n"):
        if "pan.baidu.com" in t:
            link_list = re.findall(r"https.*?[\n \]]$", t)
            if len(link_list) > 0:
                link = link_list[0]
                pwd = re.findall(r"提取码：(.{4})", t)[0]
                if "?pwd" not in link:
                    link = link + "?pwd=" + pwd

                link = re.sub("\s", "", link)
                down_link_list.append(link)

    num = 1
    for t in down_link_list:
        print(t, num)
        num += 1
        os.startfile(t)
