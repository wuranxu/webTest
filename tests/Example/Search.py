import time
import unittest

from page.index import Index
from tests.base_case import BaseCase

from tests.base_case_class import BaseCaseCls
from util.decorator import screenshot


class BingSearch(BaseCase):

    @screenshot
    def test_haha(self):
        """搜索龙珠超"""
        time.sleep(10)
        page = self.driver.new_page()
        # main = Index(page)
        # main.search_dragonball_super()
        # 断言
        self.assertEqual("龙珠超2 - 国内版 Bing", self.driver.page.title(),
                         "bing搜索'龙珠超'后页面标题与预期不符")

    @screenshot
    def test_dragon_ball_z(self):
        """搜索龙珠超 case2"""
        # 断言
        self.assertEqual("龙珠超22 - 国内版 Bing", self.driver.page.title(),
                         "bing搜索'龙珠超'后页面标题与预期不符")


if __name__ == "__main__":
    unittest.main()
