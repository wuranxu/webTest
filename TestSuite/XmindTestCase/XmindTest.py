from TestSuite.base_case import BaseCase
from Tools.decorator import screenshot
from Page.index import Index


class XmindTest(BaseCase):

    retry = 0

    @screenshot
    def test(self):
        """这是一个测试xmind的用例"""
        Index(self.driver).search_dragonball_super()
        self.assertEqual("龙珠超_百度搜索", self.driver.title, "百度首页->搜索\"龙珠超\"后页面标题与预期不符")
