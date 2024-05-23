from win32com.client import CDispatch


def fun_删除图层广告(doc: CDispatch):
    all_layers = []
    for in_layer in doc.Layers:
        all_layers.append(in_layer)

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
