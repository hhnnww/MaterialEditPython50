"""."""

from __future__ import annotations

from typing import TYPE_CHECKING

from win32com.client import Dispatch

if TYPE_CHECKING:
    from win32com.client.dynamic import CDispatch


def s(app: CDispatch, name: str) -> CDispatch:
    """."""
    return app.StringIDToTypeID(f"{name}")


def ps_display_dialogs() -> dict[str, int]:
    """."""
    return {"all": 1, "error": 2, "no": 3}


def dialog(dialog_type: str = "no") -> int | None:
    """."""
    dialogs = ps_display_dialogs()
    return dialogs.get(dialog_type, None)


def select_0(app: CDispatch, doc: CDispatch) -> None:
    """选择第一个图层."""
    desc352 = Dispatch("Photoshop.ActionDescriptor")
    ref39 = Dispatch("Photoshop.ActionReference")
    list22 = Dispatch("Photoshop.ActionList")
    ref39.PutName(s(app, "layer"), doc.Layers.Item(1).Name)
    desc352.PutReference(s(app, "target"), ref39)
    desc352.PutBoolean(s(app, "makeVisible"), value=False)
    list22.PutInteger(doc.Layers.Item(1).id)
    desc352.PutList(s(app, "layerID"), list22)
    app.ExecuteAction(s(app, "select"), desc352, dialog())


def fun_选择图层(app: CDispatch, item: CDispatch) -> None:
    """选择图层."""
    desc352 = Dispatch("Photoshop.ActionDescriptor")
    ref39 = Dispatch("Photoshop.ActionReference")
    list22 = Dispatch("Photoshop.ActionList")
    ref39.PutName(s(app, "layer"), item.Name)
    desc352.PutReference(s(app, "target"), ref39)
    desc352.PutBoolean(s(app, "makeVisible"), value=False)
    list22.PutInteger(item.id)
    desc352.PutList(s(app, "layerID"), list22)
    app.ExecuteAction(s(app, "select"), desc352, dialog())
