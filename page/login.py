from browser.browsers import Browser
from config import Config
from util.decorator import Log


class Login(object):
    logger = Log()
    driver: Browser = None
    page = None

    def __init__(self, browser_type="chrome", **kwargs):
        # 免去重复登录操作, 通过cookie
        try:
            playwright = Config.playwright
            self.driver = Browser(playwright, browser_type=browser_type, size={'width': 1920, 'height': 1080}, **kwargs)
            self.page = self.driver.new_page()
            self.page.get(Config.url)
        except Exception as e:
            self.logger.error("driver初始化失败....\n系统信息: {} \n浏览器类型: {}\n详细信息: {}".format(
                Config.system, Config.BROWSER, str(e)))
            if self.driver:
                self.driver.quit()
            raise Exception(e)

    def login(self):
        if not Config.cookie:
            # login step 登录步骤，记得封装Location定位，如果考虑简便，可以用playwright的原始元素
            self.page.page.click("[placeholder=\"请输入用户名\"]")
            self.page.page.fill("[placeholder=\"请输入用户名\"]", "wuranxu")
            self.page.page.press("[placeholder=\"请输入用户名\"]", "Tab")
            self.page.page.fill("[placeholder=\"请输入密码\"]", "wuranxu@33")
            self.page.page.click("button:has-text(\"登 录\")")
            # wait for login ok
            self.page.page.wait_for_selector(".ant-avatar")
            self.driver.save_cookie()
        else:
            self.driver.context.add_cookies(Config.cookie)
            self.driver.page.refresh()
        return self.driver



