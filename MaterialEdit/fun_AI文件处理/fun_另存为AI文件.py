from win32com.client import CDispatch
from pathlib import Path


def fun_另存为AI文件(doc: CDispatch, ai_path: Path):
    if ai_path.suffix.lower() == ".eps":
        in_ai_path = ai_path.with_suffix(".ai")
        if in_ai_path.exists() is False:
            doc.SaveAs(in_ai_path.as_posix())
            doc.Close()

            ai_path.unlink()

    else:
        doc.Save()
        doc.Close()
