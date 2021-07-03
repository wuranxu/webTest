import time
import unittest

from page.index import Index
from tests.base_case import BaseCase

from tests.base_case_class import BaseCaseCls
from util.decorator import screenshot


class BingSearch(BaseCase):

    @screenshot
    def test_xixi(self):
        """搜索龙珠超"""
        # page = self.driver.new_page()
        # main = Index(page)
        time.sleep(12)
        # 断言
        self.assertEqual("答题系统", self.driver.page.title(),
                         "bing搜索'龙珠超'后页面标题与预期不符")


if __name__ == "__main__":
    unittest.main()
