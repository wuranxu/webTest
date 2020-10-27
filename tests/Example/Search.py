import unittest

from page.index import Index

from tests.base_case import BaseCase
from util.decorator import screenshot


class BingSearch(BaseCase):

    @screenshot
    def test(self):
        """搜索龙珠超"""
        main = Index(self.driver)
        main.search_dragonball_super()
        # 断言
        self.assertEqual("龙珠 - 国内版 Bing", self.driver.title,
                         "bing搜索'龙珠超'后页面标题与预期不符")


if __name__ == "__main__":
    unittest.main()
