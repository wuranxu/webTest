from TestSuite.base_case import BaseCase
from Tools.decorator import screenshot
from Page.index import Index


class XmindTest(BaseCase):

    retry = 0

    @screenshot
    def test(self):
        """这是一个测试xmind的用例"""
        Index(self.driver).search_dragonball_super()
        self.assertEqual("龙珠超 - 国内版 Bing", self.driver.title, "bing搜索'龙珠超'后页面标题与预期不符")
