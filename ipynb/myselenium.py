import time
from typing import Union

from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class Selenium:

    @property
    def driver(self):
        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("detach", True)

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1292x1398")

        driver = Edge(options=options)
        driver.set_window_position(x=1292, y=0)

        return driver

    @property
    def wait(self) -> WebDriverWait:
        return WebDriverWait(driver=self.driver, timeout=20, poll_frequency=0.5)

    @property
    def ac(self):
        return ActionChains(self.driver)

    def find_by_css(
        self, value: str, first: bool = False
    ) -> Union[WebElement, list[WebElement]]:
        """
        根据CSS选择器查找元素
        """
        if first is True:
            return self.driver.find_element(By.CSS_SELECTOR, value)

        return self.driver.find_elements(By.CSS_SELECTOR, value)

    def find_by_xpath(
        self, value: str, first: bool = False
    ) -> Union[WebElement, list[WebElement]]:
        """
        根据XPATH查找元素
        """
        if first is True:
            return self.driver.find_element(By.XPATH, value)

        return self.driver.find_elements(By.XPATH, value)

    def js_click(self, selector: str):
        """
        浏览器执行JS代码来执行点击
        """
        self.driver.execute_script(f'document.querySelector("{selector}").click()')
        time.sleep(1)

    def send_keys(self, seletor: str, value: str):
        """
        给input传送本文
        """
        ele = self.driver.find_element(By.CSS_SELECTOR, seletor)
        ele.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        ele.send_keys(Keys.DELETE)
        time.sleep(0.5)
        ele.send_keys(value)
        time.sleep(1)

    def click(self, seletor: str):
        """
        点击页面元素
        """
        self.driver.find_element(By.CSS_SELECTOR, seletor).click()
        time.sleep(1)
