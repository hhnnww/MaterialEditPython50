from __future__ import annotations

from typing import TYPE_CHECKING

from win32com.client import CDispatch, Dispatch

if TYPE_CHECKING:
    from pathlib import Path


def fun_导出PNG(doc: CDispatch | None, ai_path: Path) -> None:
    """所有画板导出PNG"""
    if doc is None:
        return

    option = Dispatch("Illustrator.ExportForScreensOptionsJPEG")
    option.ScaleType = 1
    option.ScaleTypeValue = 1500

    item_option = Dispatch("Illustrator.ExportForScreensItemToExport")

    doc.ExportForScreens(
        ExportFolder=ai_path.parent.as_posix(),
        ExportFormat=1,
        Options=option,
        ItemToExport=item_option,
        FileNamePrefix="export_",
    )
