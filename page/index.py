from .base import Base, Location
from util.web_tool import Tools
import time


class Index(Base):
    search = Location("搜索按钮", "#sb_form_go")
    search_input = Location("搜索内容输入框", "#sb_form_q")

    def search_dragonball_super(self):
        self.driver.send(self.search_input, "龙珠超")
        self.driver.click(self.search)
