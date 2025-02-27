"""上传到百度网盘."""

from fastapi import APIRouter
from pydantic import BaseModel

from route_上传到百度网盘.class_上传所有文件夹 import UpAllFolderToBaiduWangPan

route = APIRouter(prefix="/up_baiduwangpan")


class UpBaiduModel(BaseModel):
    parent_path: str
    start_stem: int
    end_stem: int = 99999


class UpBaiduResponseModel(BaseModel):
    msg: str


@route.post(path="")
def route_up_to_baiduwangpan(item: UpBaiduModel) -> UpBaiduResponseModel:
    """上传到百度网盘."""
    obj = UpAllFolderToBaiduWangPan(
        parent_path=item.parent_path,
        start_stem=item.start_stem,
        end_stem=item.end_stem,
    )
    obj.main()

    return UpBaiduResponseModel(msg="上传成功")
