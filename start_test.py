import importlib  # 动态导入模块
import os
import sys
import unittest
from datetime import datetime

from playwright.sync_api import sync_playwright

from config import Config
from result.generator import generate
from result.suite import Suite
from result.text_test_result import result
from util.utils import Utils
from util.web_tool import Tools

sys.path.append(os.getcwd())


def create_suite():
    suite = Suite()
    all_case = Tools.get_all_case()
    case_info = {}
    for k, v in all_case.items():
        cls_name = importlib.import_module("{}.{}.{}".format(Config.suite_name, v, k))
        case, case_name = Tools.get_case_cls(cls_name, v, dir(cls_name))
        case_info.update({case_name: v})  # 对应用例和套件
        case_list = Tools.get_case_name(case)
        for c in case_list:
            suite.addTest(case(c))
    Config.case_info = case_info
    return suite


def write_report(html):
    file = "report{}.html".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"))
    Utils.make_dir(Config.report_path)
    filename = os.path.join(Config.report_path, file)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(Config.report_path, "report.html"), "w", encoding="utf-8") as file:
        file.write(html)


def run(playwright):
    start = datetime.now()
    suite = create_suite()
    Config.CASE_NUM = len(getattr(suite, "_tests"))
    Config.playwright = playwright
    runner = unittest.TextTestRunner(resultclass=result)
    rt = runner.run(suite)
    html, info, rv = generate(rt, start)
    write_report(html)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
