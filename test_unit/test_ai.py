import sys

sys.path.append(r"C:\Users\wuweihua\codeProject\MaterialEditPython5.0")
from win32com.client import GetActiveObject

from MaterialEdit.fun_AI文件处理 import AIFile

app = GetActiveObject("Illustrator.Application")

ai = AIFile(
    ai_path=r"E:\小夕素材\10000-20000\10363\10363\小夕素材(01)\小夕素材(01).ai", app=app
)

ai.fun_导出PNG()
