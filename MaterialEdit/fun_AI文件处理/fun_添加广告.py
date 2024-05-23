from pathlib import Path

from win32com.client import CDispatch


def fun_添加广告(doc: CDispatch):
    ai_path = Path(__file__).parent / "logo.ai"
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
