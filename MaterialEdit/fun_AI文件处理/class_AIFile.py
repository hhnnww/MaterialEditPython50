from pathlib import Path

from win32com.client.dynamic import CDispatch

from MaterialEdit.fun_AI文件处理.fun_PNG图片移动到上层目录 import (
    fun_PNG图片移动到上层目录,
)
from MaterialEdit.fun_AI文件处理.fun_删除图层广告 import fun_删除图层广告
from MaterialEdit.fun_AI文件处理.fun_另存为AI文件 import fun_另存为AI文件
from MaterialEdit.fun_AI文件处理.fun_同层级图片改名 import fun_同层级图片改名
from MaterialEdit.fun_AI文件处理.fun_导出PNG import fun_导出PNG
from MaterialEdit.fun_AI文件处理.fun_添加广告 import fun_添加广告


class AIFile:
    def __init__(self, ai_path: str, app: CDispatch, shop_name: str) -> None:
        """AI文件处理类."""
        self.ai_path = Path(ai_path)
        self.app = app
        self.shop_name = shop_name
        self.doc = self.app.Open(ai_path)

    def fun_导出PNG(self) -> None:
        """导出PNG文件."""
        fun_删除图层广告(self.doc)

        fun_导出PNG(self.doc, self.ai_path)
        fun_PNG图片移动到上层目录(self.ai_path)
        fun_同层级图片改名(ai_path=self.ai_path)
        fun_添加广告(self.doc, shop_name=self.shop_name)
        fun_另存为AI文件(self.doc, self.ai_path)
