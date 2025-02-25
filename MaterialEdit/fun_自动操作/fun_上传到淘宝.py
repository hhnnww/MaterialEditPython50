import re
import shutil
import time
from pathlib import Path

from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


class SeleniumUploadTaobao:
    def __init__(self) -> None:
        """Init"""
        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = Edge(options=options)  # type: ignore  # noqa: PGH003
        self.driver.set_window_rect(x=1274, y=0, width=1292, height=1398)

        self.up_loader_path = Path(r"C:\Users\wuweihua\Desktop\UPLOAD")

    def fun_页面标题等待(self, title: str) -> bool:
        """判断标题是否包含，来确定是否加载完成"""
        return WebDriverWait(driver=self.driver, timeout=10, poll_frequency=1).until(
            expected_conditions.title_contains(title),
        )

    def fun_js点击(self, selector: str) -> None:
        """页面执行JS来进行点击 因为selenium很多按钮点击不了"""
        self.driver.execute_script(f'document.querySelector("{selector}").click()')

    @staticmethod
    def fun_获取数字(stem: str) -> int:
        """获取字符串中的数字"""
        num_list = re.findall(r"\d+", stem)
        if len(num_list) > 0:
            return int("".join(num_list))

        return 0

    def fun_登录(self) -> None:
        """输入账号密码进行登录，会自动跳入到后台"""
        self.driver.get(
            "https://havanalogin.taobao.com/mini_login.htm?lang=zh_CN&appName=taobao&appEntrance=qianniu_pc_web&styleType=vertical&bizParams=&notLoadSsoView=true&notKeepLogin=false&isMobile=false&cssUrl=https://g.alicdn.com/qn/qn-login-iframe-css/0.0.8/qn-login-iframe.css&returnUrl=https://myseller.taobao.com/home.htm&rnd=0.17371788128615084",
        )
        self.fun_页面标题等待("登录")
        self.driver.find_element(By.CSS_SELECTOR, "#fm-login-id").send_keys(
            "tb313185518913",
        )
        self.driver.find_element(By.CSS_SELECTOR, "#fm-login-password").send_keys(
            input("输入密码"),
        )
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#login-form > div.fm-btn > button",
        ).click()
        self.fun_页面标题等待("千牛商家工作台")

    def fun_上传单个商品(self, material_path: Path) -> None:
        """上传单个商品"""
        self.driver.get(
            "https://item.upload.taobao.com/sell/v2/publish.htm?catId=201160807&smartRouter=true&keyProps=%7B%7D&newRouter=1&paramCacheId=merge_router_cache_389353239_1694673279246_988&x-gpf-submit-trace-id=213e259e16946732792022149e0968",
        )
        self.fun_页面标题等待("商品发布")
        # 标题
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-title > div.sell-component-info-wrapper-component-wrap > div.sell-component-info-wrapper-component-child-wrap > div > div > span > span > span > span > input",
        ).send_keys(material_path.stem)
        time.sleep(1)

        # 价格
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-price > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-price > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys("3")
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-price > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys(".")
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-price > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys("8")
        time.sleep(1)

        # 库存
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-quantity > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-quantity > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys(Keys.DELETE)
        time.sleep(0.5)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-quantity > div.sell-component-info-wrapper-component-wrap > div > div > span > span.input-wrap > span > input",
        ).send_keys("888888")
        time.sleep(1)

        # 商家编码
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sell-field-outerId > div.sell-component-info-wrapper-component-wrap > div > div > span > span > span > span > input",
        ).send_keys(material_path.stem)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_DOWN)

        # 点击上传主图
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#struct-mainImagesGroup > div > div > div > div > div > div",
        ).click()

        # 切换到上传图片frame
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame(
            self.driver.find_element(
                By.CSS_SELECTOR,
                "body > div.next-overlay-wrapper.v2.opened > div > div > div > iframe",
            ),
        )
        time.sleep(2)

        # 点击ST文件夹
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sucai-tu-selector-container > div.Home_body__P3Ncj.Home_withoutHeaderBody__DxGAT > div.PicGroupList_aside__fp5JR > div > div > div > div > ul > li:nth-child(2) > div",
        ).click()
        time.sleep(2)

        # 点击暴富首图
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sucai_tu_selector_scrollMain > div > div > label > div.PicList_pic_imgBox__c0HXw > img",
        ).click()
        time.sleep(2)

        # 点击确定
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#sucai-tu-selector-container > div.Footer_contain__g740- > div:nth-child(2) > button.next-btn.next-medium.next-btn-primary.Footer_selectOk__nEl3N",
        ).click()
        time.sleep(1)

        # 切回到主框架
        self.driver.switch_to.parent_frame()
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_DOWN)

        # 详情图片上传按钮
        js_text = 'document.querySelector("#sell-field-descRepublicOfSell > div.sell-component-info-wrapper-component-wrap > div.sell-component-info-wrapper-component-child-wrap > div > div > div.editor--GiZhF > div > div.editPanel--nAdw5.lite-editor-panel > div.editHeader--HV9VI.sidePadding--Zi2zU > div.leftPart--RCPnT > div:nth-child(1)").click()'
        self.driver.execute_script(js_text)
        time.sleep(2)

        # 进入到图片上传frame
        self.driver.switch_to.frame(
            self.driver.find_element(
                By.CSS_SELECTOR,
                "body > div.ln-overlay-wrapper.opened > div.ln-overlay-inner.mediaDialog--EM7Hx.ck-dialog.overlay--Bwotz > div > iframe",
            ),
        )

        # 点击上传图片按钮
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#container > div > div.hasEms.container > div.main > div > div.opt-body > div.list > div.search-bar > div.right-btn.btn",
        ).click()
        time.sleep(2)

        # 构建图片列表
        pic_list: list[Path] = []
        for in_file in (material_path).iterdir():
            if in_file.is_file() and in_file.suffix.lower() == ".jpg":
                pic_list.append(in_file)

                if len(pic_list) == 20:
                    break

        pic_list.sort(key=lambda k: self.fun_获取数字(k.stem))

        # 上传
        pic_text = "\n".join([pic.as_posix() for pic in pic_list])
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/input",
        ).send_keys(pic_text)

        # 等待时间
        time.sleep(len(pic_list) / 1.5)

        # 选择图片
        pic_item_list = self.driver.find_elements(By.CSS_SELECTOR, "#items > div")[
            : len(pic_list)
        ]

        for pic_item in pic_list:
            for item in pic_item_list:
                name = item.find_element(By.CSS_SELECTOR, ".name").text
                if name == pic_item.name:
                    item.location_once_scrolled_into_view
                    item.find_element(By.CSS_SELECTOR, "img").click()
                    time.sleep(0.5)

        # 点击确认
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#container > div > div.hasEms.container > div.main > div > div.opt-footer > div.btn.btn-blue",
        ).click()
        time.sleep(3)

        # 切回到主框架
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

        # 放入仓库
        self.fun_js点击(
            selector="#sell-field-startTime > div.sell-component-info-wrapper-component-wrap > div.sell-component-info-wrapper-component-child-wrap > div > div > span > span:nth-child(3) > label",
        )
        time.sleep(1)

        # 提交宝贝
        self.fun_js点击(selector="#struct-buttons > button")
        time.sleep(1)

        # 删除文件夹
        shutil.rmtree(material_path)

        time.sleep(5)

    def main(self):
        self.fun_登录()

        for in_path in tqdm(
            list(self.up_loader_path.iterdir()),
            desc="上传产品到淘宝",
            ncols=100,
        ):
            if in_path.is_dir():
                self.fun_上传单个商品(material_path=in_path)


if __name__ == "__main__":
    atb = SeleniumUploadTaobao()
    atb.main()
