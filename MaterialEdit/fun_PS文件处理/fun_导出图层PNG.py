"""."""

import contextlib
import shutil
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from win32com.client import Dispatch
from win32com.client.dynamic import CDispatch

from MaterialEdit.fun_PS文件处理.fun_PS基础操作 import dialog, s
from MaterialEdit.setting import OUT_PATH


def fun_清空OUT_PATH() -> None:
    """清空桌面OUT_PATH文件夹."""
    for in_file in OUT_PATH.iterdir():
        if in_file.is_file():
            in_file.unlink()

        else:
            shutil.rmtree(in_file)


def fun_导出单个图层(
    app: CDispatch,
    in_layer: CDispatch,
    file: Path,
    ref_doc: CDispatch,
) -> Path:
    """传入单个图层,并且导出到桌面PNG."""
    in_out_path = OUT_PATH / file.stem.lower()

    if in_out_path.exists() is False:
        in_out_path.mkdir(parents=True)

    ref_doc.ActiveLayer = in_layer

    # 导出图片
    desc = Dispatch("Photoshop.ActionDescriptor")
    ref = Dispatch("Photoshop.ActionReference")
    ref.PutEnumerated(s(app, "layer"), s(app, "ordinal"), s(app, "targetEnum"))
    desc.PutReference(s(app, "null"), ref)
    desc.PutString(s(app, "fileType"), "png")
    desc.PutInteger(s(app, "quality"), 32)
    desc.PutInteger(s(app, "metadata"), 0)

    desc.PutString(s(app, "destFolder"), in_out_path.as_posix())
    desc.PutBoolean(s(app, "sRGB"), value=True)
    desc.PutBoolean(s(app, "openWindow"), value=True)
    app.ExecuteAction(s(app, "exportSelectionAsFileTypePressed"), desc, dialog())

    return in_out_path / (in_layer.Name + ".png")


def fun_比例判断(item: CDispatch, ad_list: list[CDispatch]) -> bool:
    """先判断图层的比例，然后判断图片列表的图片比例."""
    bounds = item.Bounds
    item_width = bounds[2] - bounds[0]
    item_height = bounds[3] - bounds[1]
    ratio = item_height / item_width
    diff = 0.1
    for ad_pic in ad_list:
        ad_ratio = ad_pic.shape[0] / ad_pic.shape[1]

        if abs(ad_ratio - ratio) < diff:
            return True

    return False


def fun_文档比例(item: CDispatch, doc_bounds: tuple[int, int]) -> bool:
    """判断文档比例."""
    bounds = item.Bounds
    item_width = bounds[2] - bounds[0]
    item_height = bounds[3] - bounds[1]
    ratio = item_height / item_width
    diff = 0.1
    return abs(ratio - doc_bounds[1] / doc_bounds[0]) < diff


def fun_两个数字中间(num: int, a: int, b: int) -> bool:
    """判断num是否在a和b之间."""
    return a < num < b


def is_export_layer(item: CDispatch, doc_bounds: tuple[int, int]) -> bool:
    """."""
    if item.Kind not in [1, 17]:
        return False

    # 如果是印盖图层
    if item.Grouped is True:
        return False

    # 如果在文档之外
    left, t, r, b = item.Bounds
    if (
        r <= 0
        or b <= 0
        or left >= doc_bounds[0]
        or t >= doc_bounds[1]
        or left <= 0
        or r >= doc_bounds[0]
        or t <= 0
        or b >= doc_bounds[1]
    ):
        return False

    # 如果大于宽高三分之一
    if int(abs(r - left)) > int(doc_bounds[0] / 3) or int(abs(b - t)) > int(
        doc_bounds[1] / 3,
    ):
        return False

    # 如果是隐藏图层
    return item.Visible


class LayerItem(BaseModel):
    item: Any
    img_path: Path


def run_导出所有图层(
    app: CDispatch,
    in_doc: CDispatch,
    file: Path,
    layer_list: list[CDispatch],
) -> list[LayerItem]:
    """导出所有图层。"""
    export_layer_list = []
    text_kind = 2
    for item in layer_list:
        if item.Kind != text_kind:
            if item.Bounds == (0.0, 0.0, 0.0, 0.0):
                item.Delete()

            elif is_export_layer(item, (in_doc.Width, in_doc.Height)) is True:
                with contextlib.suppress(Exception):
                    img_path = fun_导出单个图层(app, item, file, in_doc)
                    export_layer_list.append(LayerItem(item=item, img_path=img_path))

    return export_layer_list
