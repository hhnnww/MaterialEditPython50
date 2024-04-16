from pathlib import Path

import pythoncom
from win32com.client import DispatchEx


class PPTFile:
    def __init__(self, ppt_file: Path, ppt_export_path: Path):
        self.ppt_file = ppt_file
        self.ppt_dir = ppt_export_path / ppt_file.stem

    def fun_导出PNG(self):
        pythoncom.CoInitialize()
        ppt_app = DispatchEx("PowerPoint.Application")
        ppt_app.DisplayAlerts = 0
        try:
            ppt = ppt_app.Presentations.Open(self.ppt_file.as_posix())
        except:
            print("文件打开错误。")
            return None
        else:
            try:
                # if self.ppt_dir.exists() is False:
                #     self.ppt_dir.mkdir(parents=True)
                ppt.SaveAs(self.ppt_dir, 17)
            except:
                print(f"错误文件，无法导出：{self.ppt_file.as_posix()}")
                ppt.Close()
                return None

            if self.ppt_file.suffix.lower() == ".ppt":
                ppt.SaveAs(self.ppt_file.with_suffix(".pptx"))
                self.ppt_file.unlink()

            ppt.Close()
            pythoncom.CoUninitialize()

            return "ok"


if __name__ == "__main__":
    PPTFile(Path(r"X:\H000-H999\H0257\H0257\小夕素材(1).pptx")).fun_导出PNG()
