"""另存为AI文件"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from win32com.client import CDispatch


def fun_另存为AI文件(doc: CDispatch | None, ai_path: Path) -> None:
    """另存为AI文件."""
    if doc is None:
        return

    if ai_path.suffix.lower() == ".eps":
        in_ai_path = ai_path.with_suffix(".ai")
        if in_ai_path.exists() is False:
            doc.SaveAs(in_ai_path.as_posix())
            doc.Close()

            ai_path.unlink()

    else:
        doc.Save()
        doc.Close(2)
