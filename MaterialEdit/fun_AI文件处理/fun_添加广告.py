"""add ad."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from win32com.client import CDispatch


def fun_添加广告(doc: CDispatch | None, shop_name: str) -> None:
    """添加广告."""
    if doc is None:
        return
    ai_path = (
        Path(__file__).parent.parent
        / "fun_PS文件处理"
        / "img"
        / shop_name
        / "二维码.png"
    )

    ad_layer = doc.Layers.Add()
    ad_layer.Name = "删除这个图层，即可开始编辑。"

    doc.ImportFileIntoDocument(
        ImportFile=ai_path.as_posix(),
        IsLinked=False,
        LibraryName="xiaoxisc",
        ItemName="xiaoxisc",
    )

    fr = list(ad_layer.PageItems)[0]

    ratio = fr.Width / fr.Height

    fr.Width = doc.Width
    fr.Height = fr.Width / ratio

    if fr.Height > doc.Height:
        fr.Height = doc.Height
        fr.Width = fr.Height * ratio

    fr.Left = 0
    fr.Top = 0
