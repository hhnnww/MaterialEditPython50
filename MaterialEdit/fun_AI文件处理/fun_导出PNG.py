from __future__ import annotations

from typing import TYPE_CHECKING

from win32com.client import CDispatch, Dispatch

if TYPE_CHECKING:
    from pathlib import Path


def fun_导出PNG(doc: CDispatch | None, ai_path: Path) -> None:
    """所有画板导出PNG"""
    if doc is None:
        return

    option = Dispatch("Illustrator.ExportForScreensOptionsPNG24")
    option.ScaleType = 1
    option.ScaleTypeValue = 2000
    option.Transparency = False
    option.Interlaced = True

    item_option = Dispatch("Illustrator.ExportForScreensItemToExport")

    doc.ExportForScreens(
        ExportFolder=ai_path.parent.as_posix(),
        ExportFormat=7,
        Options=option,
        ItemToExport=item_option,
        FileNamePrefix="export_",
    )
