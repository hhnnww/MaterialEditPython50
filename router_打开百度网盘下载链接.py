"""打开百度网盘下载链接."""

import re
import subprocess

from fastapi import APIRouter
from pydantic import BaseModel

from mylog import mylogger

router = APIRouter(prefix="/open_baidu_link")


class ItemIn(BaseModel):
    md_text: str


@router.post("/open_link")
def open_baidu_link(item_in: ItemIn) -> None:
    """打开网盘下载链接."""
    text = item_in.md_text
    link_list = re.findall("(https://pan.baidu.com.*?)\n", text)

    for link in link_list:
        re_link = re.sub(r"\s", "", link)

        if "提取码" in re_link:
            re_link = re.sub("提取码:.*", "", re_link)

        if "?pwd" not in re_link:
            tqm: str = re.findall(rf"{re_link}[\s\S]*?提取码：(.*?)\n", text)[0]
            tqm = re.sub(r"\s", "", tqm)
            re_link = f"{re_link}?pwd={tqm}"

        msg = f"打开链接: {re_link}"
        mylogger.info(msg)
        subprocess.Popen(args=["start", "msedge", re_link], shell=True)
