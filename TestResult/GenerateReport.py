__author__ = 'Woody'
import re
from datetime import datetime

from jinja2.environment import Template

from config import Config


def generate(result, startTime):
    test_cases_list = []
    report_headers = {}
    test_cases = []
    start = startTime.strftime("%Y-%m-%d %H:%M:%S")
    duration = str(datetime.now() - startTime).split(".")[0]
    # 获取成功/失败/错误/跳过数量以及着色
    success, failed, error, skip = len(result.successes), len(result.failures),\
                                   len(result.errors), len(result.skipped)
    status = "<span style='color: #5cb85c'>成功: {}</span> <span style='color: #d9534f'>失败: {}</span> " \
             "<span style='color: #f0ad4e'>出错: {}</span> <span style='color: #5bc0de'>跳过: {}</span>".format(
        success, failed, error, skip)
    info = "成功: {} 失败: {} 出错: {} 跳过: {}".format(
        success, failed, error, skip)

    # 邮件展示用例运行状态
    rv = "未通过" if result.errors or result.failures else "通过"
    report_headers.update(dict(start_time=start, duration=duration, status=status))

    # 整合所有case
    test_cases.extend(sorted(result.failures, key=lambda x: x.get("case_id", "Case000")))
    test_cases.extend(sorted(result.errors, key=lambda x: x.get("case_id", "Case000")))
    test_cases.extend(sorted(result.successes, key=lambda x: x.get("case_id", "Case000")))
    test_cases.extend(sorted(result.skipped, key=lambda x: x.get("case_id", "Case000")))

    for case in test_cases:
        case_id = case.get("case_id")
        _case = case.get("case")
        msg = case.get("msg")
        msg = msg[1].__str__() if msg and case["type"] != "info" else msg
        status = case.get("type")
        suite = getattr(Config, "case_info").get(str(case_id))
        if suite is None:
            suite = getattr(Config, "case_info").get(
                str(re.findall(r"\((.+)\)", _case.description)[0].split(".")[-1]))
        if getattr(_case, "_testMethodName"):
            case_name = getattr(_case, "_testMethodName")
        else:
            case_name = re.findall(r"\((.+)\)", _case.description)[0].split(".")[-1]
        if getattr(_case, case_name, None) is None:
            case_des = "登录初始化模块"
        else:
            case_des = getattr(getattr(_case, case_name), "__doc__")
        test_cases_list.append((case_id, suite, status, msg, case_des))
    # 通过case_id排序
    # test_cases_list = sorted(test_cases_list, key=lambda x: x[0])
    total_test = len(test_cases_list)
    with open(Config.report_mod, encoding="utf-8") as f:
        html = Template(f.read())
        # 渲染html模板
        return html.render(headers=report_headers, test_cases_list=test_cases_list,
                           total_test=total_test, conf=Config,
                           success=success, failed=failed, error=error, rv=rv,
                           skip=skip), info, rv
