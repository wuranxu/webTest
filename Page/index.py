from .base import Base, Location
from Tools.web_tool import Tools
import time

class Index(Base):

    # menu = Location("大后台左侧菜单", ".menuItem")
    # seperate = Location("展开的菜单", ".hasChild.itemLink.active")
    search = Location("搜索按钮", "#sb_form_go")
    search_input = Location("搜索内容输入框", "#sb_form_q")

    def search_dragonball_super(self):
        self.driver.send(self.search_input, "龙珠超")
        self.driver.click(self.search)

    # def close_menu(self):
    #     if self.driver.exists(self.seperate):
    #         self.driver.click(self.seperate)
    #
    # def select_menu(self, menu):
    #     menu_list = Tools.trans_menu(menu)
    #     self.close_menu()                   # 需要先关闭菜单, 但是需要等待菜单折叠起来
    #     for n in menu_list:
    #         self.driver.click_text(self.menu, n)









