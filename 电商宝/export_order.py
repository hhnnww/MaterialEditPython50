"""export order"""

import pyperclip
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from requests_html import HTMLSession

session = HTMLSession()
uri = "mongodb+srv://hhnnww:<db_password>@tibetunit.fdr8m8w.mongodb.net/?retryWrites=true&w=majority&appName=tibetunit"
client = MongoClient(uri, server_api=ServerApi("1"))
database = client["电商宝返款订单"]
col_order = database["订单列表"]
col_page = database["所有页面"]

col_page.create_index(keys="page", unique=True)
col_order.create_index(keys="order_sn", unique=True)


def get_header() -> dict[str, str]:
    """Get header"""
    req_header = pyperclip.paste().strip()
    req_split = req_header.split(sep="\n")
    header_dict = {}
    for req_line in req_split[1:]:
        req_line = req_line.strip()
        line_split = req_line.split(sep=": ")
        header_dict.update({line_split[0]: line_split[1]})
    return header_dict


def get_order(url: str, header_dict: dict[str, str]) -> None:
    """Get order"""
    res = session.post(url=url, headers=header_dict)
    objs = res.json().get("data").get("data")
    res = col_order.insert_many(documents=objs)
