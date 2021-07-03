from playwright.sync_api import ViewportSize, BrowserContext

from browser.page import DriverPage
from config import Config


class Browser(object):
    browser = None
    context: BrowserContext= None
    page: DriverPage = None

    def __init__(self, playwright, browser_type="chrome", headless=False, size: ViewportSize = None, **kwargs):
        if browser_type == "chrome":
            self.browser = playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            self.browser = playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            self.browser = playwright.webkit.launch(headless=headless)
        else:
            raise Exception("请输入正确的浏览器类型")
        self.context = self.browser.new_context(viewport=size, **kwargs)

    def new_page(self):
        page = self.context.new_page()
        self.page = DriverPage(page)
        return self.page

    def save_cookie(self):
        Config.cookie = self.context.cookies()

    def add_cookie(self):
        self.context.add_cookies(Config.cookie)

    def quit(self):
        self.page.page.close()
        self.context.close()
        self.browser.close()
