import unittest

from Page.login import Login


class BaseCase(unittest.TestCase):
    driver = None
    retry = 0

    def setUp(self):
        self._initial()

    def _initial(self):
        self.case_id = self.__class__.__name__
        lg = Login()
        try:
            self.driver = lg.login()
        except Exception as e:
            if lg.driver:
                lg.driver.quit()
            assert 0, "{} 登录失败! 原因: {}".format(self.case_id, e.__str__())

    def _clean(self):
        if self.driver:
            self.driver.quit()

    def tearDown(self):
        self._clean()