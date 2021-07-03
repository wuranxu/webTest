__author__ = 'Woody'

import inspect
import os
from datetime import datetime

from util.utils import Utils
from config import Config


class Tools(object):

    def __init__(self, page):
        """
        传入driver实例, 封装driver的方法
        :param driver:
        """
        self.page = page
        # self.ocr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_pic(self, func_name, case_id=None):
        """
        截图方法
        :param func_name: 函数名称
        :param case_id: 用例编号, 可选
        :return:
        """
        pic_dir = Config.pic_dir
        Utils.make_dir(pic_dir)
        pic = os.path.join(pic_dir, case_id) if case_id else pic_dir
        Utils.make_dir(pic)
        filename = os.path.join(pic,
                                "{} {}.png".format(func_name, datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S")))
        self.page.screen(filename)
        return filename

    @classmethod
    def get_case_num(cls, case_cls):
        """获取以test开头的所有测试用例个数"""
        return len([x for x in dir(case_cls) if x.startswith('test')])

    @classmethod
    def get_case_cls(cls, module, file, cls_name):
        for c in cls_name:
            _class = getattr(module, c)
            if cls.is_test_class(_class) and hasattr(_class, "setUp") and _class.__name__ != "Base_Case":
                return _class, _class.__name__
        else:
            raise Exception("{}文件中未找到测试类!".format(file))

    @classmethod
    def is_test_class(cls, _class):
        return len([x for x in dir(_class) if x.startswith("test")]) > 0

    @classmethod
    def get_case_name(cls, case_cls):
        """获取测试用例名称，方便加入测试套件"""
        return [x for x in dir(case_cls) if x.startswith('test')]

    @staticmethod
    def get_func():
        return inspect.stack()[0][3]

    @classmethod
    def get_all_case(cls):
        """ 获取TestSuite目录下的所有Case
            自动加载到测试套件
        """
        case_dict = {}
        suite = Config.suite_dir
        # 遍历TestSuite 获取所有以Case开头且不以.pyc结尾的用例
        for root, dirs, files in os.walk(suite):
            if root not in [os.path.join(suite, x) for x in Config.skip_suite]:
                for file in sorted(files):
                    if not file.endswith(".pyc") and not file.startswith("base_case") \
                            and file.endswith(".py"):
                        file = file.split(".")[0]
                        suite_name = root.replace("\\", "/").split("/")[-1]  # 兼容/和\
                        case_dict.update({file: suite_name})
        return case_dict

    '''OCR删除
    def get_pic_text(self, element):
        element = element if isinstance(element, WebElement) else element.ele
        pic_path = self.conf.get_value("test_pic_path")
        self.driver.get_screenshot_file_by_ele("temp", element)
        with open(os.path.join(pic_path, "temp.png"), mode="rb") as f:
            rv = self.ocr.basicAccurate(f.read())
            num = rv.get("words_result_num")
            words = rv.get("words_result")
            w = [word.get("words") for word in words]
            return dict(num=num, words=w)
    '''
