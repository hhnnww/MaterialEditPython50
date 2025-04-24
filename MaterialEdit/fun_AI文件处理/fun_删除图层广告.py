"""添加广告."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from win32com.client import CDispatch


def fun_删除图层广告(doc: CDispatch | None) -> None:
    """删除图层广告."""
    if doc is None:
        return

    all_layers = list(doc.Layers)

    for in_layer in all_layers:
        if str(in_layer.Name).lower() in [
            "DESIGNED BY FREEPIK".lower(),
            "小夕素材",
            "饭桶设计",
            "删除这个图层，即可开始编辑。",
        ]:
            if in_layer.Locked is True:
                in_layer.Locked = False
            in_layer.Delete()
