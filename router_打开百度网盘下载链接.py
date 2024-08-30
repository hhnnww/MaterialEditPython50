import os
import re

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/open_baidu_link")


class ItemIn(BaseModel):
    md_text: str


@router.post("/open_link")
def open_baidu_link(item_in: ItemIn):
    msg_split = item_in.md_text.split(r"消息可能包含存在未知风险的链接，请谨慎访问")
    for t in msg_split:
        if "pan.baidu.com" in t:
            links_re = re.findall(r"https://pan.baidu.com.*", t)
            if len(links_re) > 0:
                link = re.sub(r"\s", "", links_re[0])
                print(link)

                if "?pwd" not in link:
                    pwd_re = re.findall("提取码：(.{4})", t)
                    if len(pwd_re) > 0:
                        pwd = pwd_re[0]
                    print(pwd)
                    link = f"{link}?pwd={pwd}"

                os.startfile(link)
