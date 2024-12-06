from win32com.client import Dispatch


def fun_清空切片(app):
    """
    删除PS里面的所有切片


    """
    print("清空切片")
    idhistoryStateChanged = app.StringIDToTypeID("historyStateChanged")
    desc260 = Dispatch("Photoshop.ActionDescriptor")
    idDocI = app.CharIDToTypeID("DocI")
    desc260.PutInteger(idDocI, 59)
    idIdnt = app.CharIDToTypeID("Idnt")
    desc260.PutInteger(idIdnt, 136)
    idNm = app.CharIDToTypeID("Nm  ")
    desc260.PutString(idNm, """Clear Slices""")
    idhasEnglish = app.StringIDToTypeID("hasEnglish")
    desc260.PutBoolean(idhasEnglish, True)
    idItmI = app.CharIDToTypeID("ItmI")
    desc260.PutInteger(idItmI, 6)
    idcommandID = app.StringIDToTypeID("commandID")
    desc260.PutInteger(idcommandID, 2969)
    try:
        app.ExecuteAction(idhistoryStateChanged, desc260, 3)
    except:  # noqa: E722
        print("无法清除切片")
    finally:
        print("成功清空切片")
