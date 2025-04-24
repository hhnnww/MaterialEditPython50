"""透明转白底"""

from pathlib import Path

import pythoncom
from win32com.client import Dispatch


def fun_透明图转白底(material_path: str) -> None:
    """透明图转白底"""
    pythoncom.CoInitialize()
    ps_app = Dispatch("Photoshop.Application")
    ps_app.displayDialogs = 3
    for infile in Path(material_path).rglob("*"):
        if infile.is_file() and infile.suffix.lower() in [".png"]:
            doc = ps_app.Open(infile.as_posix())

            options = Dispatch("Photoshop.ExportOptionsSaveForWeb")
            options.Format = 6  # 6 corresponds to JPEG format
            options.Quality = 60  # Set the quality to 60

            doc.Export(ExportIn=infile.with_suffix(".jpg"), ExportAs=2, Options=options)
            doc.Close(2)
            infile.unlink()

    pythoncom.CoUninitialize()
