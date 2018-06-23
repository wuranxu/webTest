import importlib  # 动态导入模块
import os
import sys
import unittest
from datetime import datetime

from TestResult.GenerateReport import generate
from TestResult.Result import result
from TestResult.Suite import Suite
from Tools.chrome import Browser
from Tools.utils import Utils
from Tools.web_tool import Tools
from Tools.xmind_reader import Xmind
from config import Config

sys.path.append(os.getcwd())


def create_suite():
    get_xmind_case()    # 生成Xmind
    suite = Suite()
    all_case = Tools.get_all_case()
    case_info = {}
    for k, v in all_case.items():
        cls_name = importlib.import_module("{}.{}.{}".format(Config.suite_name, v, k))
        case, case_name = Tools.get_case_cls(cls_name, v, dir(cls_name))
        case_info.update({case_name: v})        # 对应用例和套件
        case_list = Tools.get_case_name(case)
        for c in case_list:
            suite.addTest(case(c))
    Config.case_info = case_info
    return suite


def get_xmind_case():
    for root, dirs, files in os.walk(Config.xmind):
        for file in files:
            if file.endswith("xmind"):
                xd = Xmind(file)
                data = xd.parse()
                xd.parse_to_case(data)


def write_report(html):
    file = "report{}.html".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"))
    Utils.make_dir(Config.report_path)
    filename = os.path.join(Config.report_path, file)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(Config.report_path, "report.html"), "w", encoding="utf-8") as file:
        file.write(html)


def run():
    Browser.set_browser()
    start = datetime.now()
    suite = create_suite()
    Config.CASE_NUM = len(getattr(suite, "_tests"))
    runner = unittest.TextTestRunner(resultclass=result)
    rt = runner.run(suite)
    html, info, rv = generate(rt, start)
    write_report(html)


if __name__ == "__main__":
    run()
