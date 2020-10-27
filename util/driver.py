from pyvirtualdisplay import Display
from selenium.webdriver.chrome.webdriver import WebDriver as WB
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as FF
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page.base import Location
from util.chrome import Browser
from util.decorator import wait, found
from config import Config
from error.element.exception import ElementException


def base():
    Config.browser_type, base_cls = ("Firefox", FF) \
        if Config.SYS == "linux" else ("Chrome", WB)
    return base_cls


class ChromeDriver(base()):

    def __init__(self):

        if Config.SYS == "linux":
            Browser.set_browser()
            # 创建虚拟桌面
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            super(ChromeDriver, self).__init__()
        else:
            # 无头模式
            # op = chrome_op()
            # op.add_argument("--headless")
            if getattr(Config, "DRIVER_PATH", None) is None:
                Browser.set_browser()
            super(ChromeDriver, self).__init__(executable_path=getattr(Config, "DRIVER_PATH", None))

    def get_element(self, ele):
        """
        获取element
        :param ele:
        :return:
        """
        return self.find_element(by=getattr(By, ele.method), value=ele.value)

    def get_elements(self, ele):
        """
        获取elements
        :param ele:
        :return:
        """
        return self.find_elements(by=getattr(By, ele.method), value=ele.value)

    @wait
    def send(self, ele, text):
        """
        向输入框输入文本
        :param ele:
        :param text:
        :return:
        """
        self.get_element(ele).send_keys(text)

    @wait
    def click(self, ele):
        """
        点击元素
        :param ele:
        :return:
        """
        return self.get_element(ele).click()

    @wait
    def clear(self, ele):
        """
        清除输入框内容
        :param ele:
        :return:
        """
        return self.get_element(ele).clear()

    @wait
    def click_text(self, ele_list, name):
        """
        点击文本(如导航条和菜单)
        :param ele_list:
        :param name:
        :return:
        """
        elements = self.get_elements(ele_list)
        for e in elements:
            if e.text == name:
                e.click()
                break
        else:
            raise Exception("未找到{}中的文本: {}".format(ele_list.name, name))

    @wait
    def click_label(self, location: Location, like=False):
        """
        点击文本(如导航条和菜单)
        :param location: 元素定位
        :param like: 文本是否模糊匹配(默认不模糊)
        :return:
        """
        elements = self.get_elements(location)
        for e in elements:
            if like and e.text == location.name:
                e.click()
                break
            elif not like and location.name in e.text:
                e.click()
                break
        else:
            raise ElementException("根据定位: [{} -> {}] 未找到带有文本{}的元素".format(
                location.method, location.value, location.name))

    @wait
    def click_index(self, location: Location, index: int):
        """
        根据索引点击元素
        :param location:
        :param index:
        :return:
        """
        elements = self.get_elements(location)
        if index > len(elements) - 1:
            raise ElementException("未找到对应索引的元素, 索引数量: {} 找到元素数量: {}".format(index, len(elements)))
        elements[index].click()

    def switch_handle(self):
        """
        切换到新窗口
        :return:
        """
        handles = self.window_handles
        for hand in handles:
            if hand != self.current_window_handle:
                self.switch_to.window(hand)
        else:
            print("没有可用的新窗口!")

    def switch_frame(self, ele):
        """
        进入iframe(可传webelement元素)
        :param ele:
        :return:
        """
        frame = self.get_element(ele)
        self.switch_to.frame(frame)

    def switch_back(self):
        """
        退出iframe, 返回主层
        :return:
        """
        self.switch_to.default_content()

    def alert_confirm(self):
        """
        在弹出的alert窗口中选择确认
        :return:
        """
        self.switch_to.alert().accept()

    def alert_refuse(self):
        """
        在弹出的alert窗口中选择取消
        :return:
        """
        self.switch_to.alert().dismiss()

    @found
    def get_text(self, ele):
        """
        获取html标签的文本
        :param ele:
        :return:
        """
        return self.get_element(ele).text

    @wait
    def attr(self, ele, attribute):
        """
        获取html标签的属性
        :param ele:
        :param attribute:
        :return:
        """
        return self.get_element(ele).get_attribute(attribute)

    def set_attr(self, ele, attribute, value):
        """
        设置html标签的属性
        :param ele:
        :param attribute:
        :param value:
        :return:
        """
        ele = self.get_element(ele)
        self.execute_script("arguments[0].{}='{}';".format(attribute, value), ele)

    @wait
    def move(self, pos):
        """
        移动到某个元素
        :param pos: 元素定位
        :return:
        """
        position = self.get_element(pos)
        # 移动到目的元素
        ActionChains(self).move_to_element(position).perform()

    def exists(self, ele):
        try:
            WebDriverWait(self, Config.TIMEOUT).until(EC.visibility_of_element_located(
                (getattr(By, ele.method), ele.value)))
            return True
        except:
            return False

    def is_show(self, ele):
        return self.execute_script("return arguments[0].display;", self.get_element(ele))
