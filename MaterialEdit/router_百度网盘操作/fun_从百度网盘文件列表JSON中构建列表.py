"""文件重命名.py"""

import json

from pydantic import BaseModel


class BaiduFileItem(BaseModel):
    id: int
    path: str
    filename: str


def fun_构建网盘文件列表(res_json: str) -> list[BaiduFileItem]:
    """构建网盘文件列表"""
    json_obj_list = json.loads(res_json)
    out_list = []
    for json_obj in json_obj_list:
        out_list.extend(
            BaiduFileItem(
                id=item_obj.get("fs_id"),
                path=item_obj.get("path"),
                filename=item_obj.get("server_filename"),
            )
            for item_obj in json_obj.get("list")
        )

    return out_list
