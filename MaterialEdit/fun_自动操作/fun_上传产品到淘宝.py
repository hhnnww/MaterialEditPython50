"""Module containing the AutoUploadProductToTaobao class.

This class automates the process of uploading products to Taobao.
"""

from pathlib import Path

import pyautogui
import pyperclip

from MaterialEdit.fun_自动操作.fun_窗口操作 import fun_窗口置顶, fun_获取窗口坐标
from MaterialEdit.fun_自动操作.fun_获取图片 import fun_获取图片
from MaterialEdit.get_stem_num import get_path_num

pyautogui.PAUSE = 3


class AutoUploadProductToTaobao:
    def __init__(self, start_stem: int) -> None:
        """初始化."""
        self.start_stem = start_stem

    path_name = "taobao_product_update"
    res = fun_获取窗口坐标("Edge")
    position = res if res is not None else (0, 0, 1920, 1080)

    MAX_IMAGES = 20

    def fun_上传单个产品(self, material_update_path: Path) -> None:  # noqa: PLR0915
        """上传单个产品."""
        pyautogui.hotkey("ctrl", "t")
        pyperclip.copy(
            "https://item.upload.taobao.com/sell/publish.htm?catId=201160807&smartRouter=true&keyProps=%7B%7D"
            "&newRouter=1&paramCacheId=merge_router_cache_389353239_1694673279246_988&x-gpf-submit-trace-id"
            "=213e259e16946732792022149e0968",
        )
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        # 关闭广告
        pyautogui.click(fun_获取图片("close_ad", self.path_name, self.position))

        # 输入标题
        pyautogui.click(fun_获取图片("title_input", self.path_name, self.position))
        pyautogui.write(material_update_path.name)

        # 输入价格
        pyautogui.click(fun_获取图片("price_input", self.path_name, self.position))
        pyautogui.write("2.9")

        # 输入数量
        pyautogui.hotkey("tab")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.write("88888")

        # 商家编码
        pyautogui.hotkey("tab")
        pyautogui.write(material_update_path.name)

        # 翻页
        pyautogui.hotkey("pageDown")
        pyautogui.sleep(2)

        # 上传首图
        pyautogui.sleep(2)
        pyautogui.click(
            fun_获取图片("first_image_button", self.path_name, self.position),
        )
        pyautogui.click(fun_获取图片("update_button_i", self.path_name, self.position))
        pyautogui.click(fun_获取图片("update_button_2", self.path_name, self.position))
        pyautogui.click(fun_获取图片("update_img_input", self.path_name, self.position))

        # 选择首图文件夹
        pyperclip.copy(material_update_path.as_posix())
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        # 点击图片1
        pyautogui.doubleClick(fun_获取图片("img1", self.path_name, self.position))
        pyautogui.click(fun_获取图片("title", self.path_name, self.position))

        pyautogui.hotkey("pageDown")

        # 详情使用旧版本按钮
        pyautogui.click(fun_获取图片("back", self.path_name, self.position))
        pyautogui.click(fun_获取图片("queding", self.path_name, self.position))
        pyautogui.click(fun_获取图片("use_text", self.path_name, self.position))

        pyautogui.sleep(3)

        # 手机使用旧版
        pyautogui.click(
            fun_获取图片("pro_use_text_mobil", self.path_name, self.position),
        )

        # 会员免费
        pyautogui.click(fun_获取图片("use_moban", self.path_name, self.position))
        pyautogui.sleep(2)
        pyautogui.click(fun_获取图片("use_free", self.path_name, self.position))

        # 上传图片
        pyautogui.click(fun_获取图片("up_img", self.path_name, self.position))
        pyautogui.click(fun_获取图片("pro_update", self.path_name, self.position))
        pyautogui.sleep(1)
        pyautogui.click(fun_获取图片("update_button_2", self.path_name, self.position))

        # 选择所有图片
        pyautogui.click(fun_获取图片("img1", self.path_name, self.position))
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("enter")

        # 便利图片
        img_list = [
            in_file
            for in_file in material_update_path.iterdir()
            if in_file.is_file() and in_file.suffix.lower() == ".jpg"
        ]

        pyautogui.sleep(len(img_list))
        pyautogui.click(fun_获取图片("pro_search", self.path_name, self.position))

        img_list.sort(key=lambda k: get_path_num(k.stem))

        for in_file in img_list[:20]:
            pyperclip.copy(in_file.name)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.hotkey("enter")
            pyautogui.sleep(1)
            pyautogui.click(fun_获取图片("xq", self.path_name, self.position))
            pyautogui.click(fun_获取图片("pro_close", self.path_name, self.position))

        pyautogui.sleep(2)
        if len(img_list) > self.MAX_IMAGES:
            pyautogui.click(fun_获取图片("up_img", self.path_name, self.position))
            pyautogui.click(fun_获取图片("pro_search", self.path_name, self.position))
            for in_file in img_list[20:]:
                pyperclip.copy(in_file.name)
                pyautogui.hotkey("ctrl", "v")
                pyautogui.hotkey("enter")
                pyautogui.sleep(1)
                pyautogui.click(fun_获取图片("xq", self.path_name, self.position))
                pyautogui.click(
                    fun_获取图片("pro_close", self.path_name, self.position),
                )

            pyautogui.sleep(1)
            pyautogui.click(
                fun_获取图片("pro_img_submit", self.path_name, self.position),
            )

        # 详情标题
        pyautogui.click(fun_获取图片("pro_title", self.path_name, self.position))
        pyautogui.hotkey("pageDown")

        # 放入仓库和提交
        pyautogui.sleep(2)
        pyautogui.click(fun_获取图片("pro_cangku", self.path_name, self.position))
        pyautogui.click(fun_获取图片("pro_up", self.path_name, self.position))

        pyautogui.sleep(2)
        fun_获取图片("success", self.path_name, self.position)
        pyautogui.hotkey("ctrl", "w")

    def run(self) -> None:
        """上传产品到淘宝."""
        fun_窗口置顶("Edge")

        for ma_path in Path(r"C:\Users\wuweihua\Desktop\UPLOAD").iterdir():
            if ma_path.is_dir() and get_path_num(ma_path.stem) >= self.start_stem:
                self.fun_上传单个产品(ma_path)
