import json

from pydantic import BaseModel


class BaiduFileItem(BaseModel):
    id: str
    path: str
    filename: str


def fun_构建网盘文件列表(res_json: str) -> list[BaiduFileItem]:
    out_list = []
    json_obj = json.loads(res_json).get("list")
    for item_obj in json_obj:
        out_list.append(
            BaiduFileItem(
                id=item_obj.get("fs_id"),
                path=item_obj.get("path"),
                filename=item_obj.get("server_filename"),
            )
        )

    return out_list
