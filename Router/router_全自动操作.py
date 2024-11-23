from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from MaterialEdit.fun_自动操作 import (
    AutoGetBaiDuShareLink,
    AutoMakeProductImage,
    AutoUploadMaterialToBaiduYun,
    AutoUploadProductToTaobao,
    DownPathMoveToMaterialPath,
)
from MaterialEdit.fun_获取路径数字 import fun_获取路径数字

from .fun_文件夹操作 import RequestMaterialPathActionModel, fun_material_path_action

router = APIRouter(prefix="/AutoAction")

# ---------------- 获取网盘分享链接 ----------------


class GetBaiduLink(BaseModel):
    start_stem: int
    end_stem: int
    parent_path: str


@router.post("/get_baidu_link")
def get_baidu_link(item: GetBaiduLink):
    AutoGetBaiDuShareLink(
        start_stem=item.start_stem, end_stem=item.end_stem, parent_path=item.parent_path
    ).run()


# ---------------- 上传到淘宝 ----------------


class UpTB(BaseModel):
    start_stem: int


@router.post("/up_taobao")
def up_taobao(item: UpTB):
    AutoUploadProductToTaobao(start_stem=item.start_stem).run()


# ---------------- 制作详情 ----------------


class MakeXQ(BaseModel):
    material_parent_path: str
    start_item: int
    shop_name: str
    make_effect: bool


@router.post("/make_all_xq")
def make_all_xq(item: MakeXQ):
    AutoMakeProductImage(
        material_parent_path=item.material_parent_path,
        start_stem=item.start_item,
        shop_name=item.shop_name,
        make_effect=True,
    ).run()


# ---------------- 上传到百度网盘 ----------------


class BaiduItem(BaseModel):
    parent_path: str
    start_stem: int


@router.post("/auto_upload_baidu")
def auto_upload_baidu(item: BaiduItem):
    AutoUploadMaterialToBaiduYun(
        parent_path=item.parent_path, start_stem=item.start_stem
    ).run()


# ---------------- 下载目录移动到素材目录 ----------------


class DownItem(BaseModel):
    ori_path: str
    dst_path: str


@router.post("/down_path_move_to_material_path")
def down_path_move_to_material_path(item: DownItem):
    DownPathMoveToMaterialPath(
        down_path=item.ori_path, material_parent_path=item.dst_path
    ).main()


# ---------------- 素材编辑 ----------------


class EditItem(BaseModel):
    parent_path: str
    start_stem: int
    shop_name: str


@router.post("/auto_edit_material")
def auto_edit_material(item: EditItem):
    # 构建所有需要处理的文件夹
    all_file = list(Path(item.parent_path).iterdir())
    used_folder = []
    for in_file in all_file:
        if in_file.is_dir() and fun_获取路径数字(in_file.stem) >= item.start_stem:
            used_folder.append(in_file.as_posix())
    used_folder.sort(key=lambda k: fun_获取路径数字(Path(k).stem))

    for root_path in used_folder:
        print(root_path)

        if item.shop_name == "饭桶设计":
            actions = [
                # "解压ZIP",
                # "移动到效果图",
                # "删除素材文件夹内所有图片",
                # "删除EPS文件",
                # "文件重命名",
                # "移动到根目录",
                # "删除广告文件",
                # "PSD-导出图片-添加广告",
                # "PSD-导出图片",
                # "AI-导出图片",
                "AI批量导出图片重命名",
                "复制图片到预览图",
                "素材图水印",
            ]

        elif item.shop_name == "松子素材":
            actions = [
                "删除素材文件夹内所有图片",
                "文件重命名",
                "移动到根目录",
                "删除广告文件",
                # "PSD-图层改名-导出图片-添加广告",
                # "PSD-导出图片-添加广告",
                "PSD-导出图片",
                # "AI-导出图片",
                "复制图片到预览图",
                "素材图水印",
            ]

        elif item.shop_name == "泡泡素材":
            actions = [
                # "解压ZIP",
                # "删除EPS文件",
                # "移动到效果图",
                "删除广告文件",
                "删除素材文件夹内所有图片",
                # "删除ZIP文件",
                "文件重命名",
                "移动到根目录",
                # "AI-导出图片",
                # "PSD-导出图片-添加广告",
                "PSD-图层改名-导出图片-添加广告",
                "复制图片到预览图",
                "素材图水印",
            ]

        for action_list in actions:
            action_item = RequestMaterialPathActionModel(
                action=action_list,
                shop_name=item.shop_name,
                root_path=root_path,
                file_start_stem="1",
                path_start_stem="1",
            )
            fun_material_path_action(item=action_item)
