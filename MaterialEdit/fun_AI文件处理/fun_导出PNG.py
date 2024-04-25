from pathlib import Path

from win32com.client import CDispatch, Dispatch


def fun_导出PNG(doc: CDispatch, ai_path: Path):
    # 所有画板导出PNG
    option = Dispatch("Illustrator.ExportForScreensOptionsPNG24")
    option.ScaleType = 1

    if doc.Height / doc.Width < 1.5:
        option.ScaleTypeValue = 3000
    else:
        option.ScaleTypeValue = 1500

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
