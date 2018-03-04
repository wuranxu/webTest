import base64
from functools import wraps
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Tools.logger import Logger
from Tools.web_tool import Tools
from config import Config

Log = Logger().logger


def wait(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            Log.info("当前Page: {} 操作: {} 控件名: {}".format(
                args[1].file, func.__name__, "->".join([str(x) for x in args[1:]])))
            try:
                WebDriverWait(args[0], Config.TIMEOUT).until(EC.element_to_be_clickable(
                    (getattr(By, args[1].method), args[1].value)))
                # WebDriverWait(args[0], Config.TIMEOUT).until(
                #     lambda x: x.find_element(getattr(By, args[1].method), args[1].value).send_keys("1")
                # )
            except Exception:
                Log.error("等待元素超时! \n文件名: {}\n函数名: {}\n控件名: {}".format(
                    args[1].file, func.__name__, args[1].name))
                assert 0, "等待元素超时! \n文件名: {}\n函数名: {}\n控件名: {}".format(
                    args[1].file, func.__name__, args[1].name)
            return func(*args, **kwargs)
    return wrapper


def generate_bs64(filename):
    with open(filename, mode='rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return b64


def update_pic_info(case_id, filename):
    if hasattr(Config, "screenshot"):
        getattr(Config, "screenshot").update({case_id: generate_bs64(filename)})
    else:
        setattr(Config, "screenshot", {case_id: generate_bs64(filename)})


def screen(driver, func, case_id):
    t = Tools(driver)
    filename = t.get_pic(func.__name__, case_id)
    update_pic_info(case_id, filename)


def pic(*params):
    if not callable(params[0]):
        re_run = params[0]

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                Log.info("当前运行测试用例: {} 函数: {}".format(args[0].__class__.__name__, func.__name__))
                driver = args[0].driver
                case_id = args[0].case_id
                error = None
                for i in range(1, re_run+1):
                    try:
                        return func(*args, **kwargs)
                    except (AssertionError, Exception) as e:
                        error = e
                        Log.warning("{}_{}用例第{}次失败: {}".format(
                            args[0].__class__.__name__, func.__name__, i, error.__str__()))
                else:
                    screen(driver, func, case_id)
                    if isinstance(error, AssertionError):
                        assert 0, "错误信息: {}".format(str(error))
                    else:
                        raise Exception("错误信息: {}".format(str(error)))
            return wrapper
        return decorator
    else:
        @wraps(params[0])
        def wrapper(*args, **kwargs):
            Log.info("当前运行测试用例id: {} 名称: {}".format(args[0].__class__.__name__, params[0].__name__))
            driver = args[0].driver
            case_id = args[0].case_id
            error = None
            for i in range(1, 3):
                try:
                    return params[0](*args, **kwargs)
                except (AssertionError, Exception) as e:
                    error = e
                    Log.warning("{}_{}用例第{}次失败: {}".format(
                        args[0].__class__.__name__, params[0].__name__, i, error.__str__()))
            else:
                screen(driver, params[0], case_id)
                if isinstance(error, AssertionError):
                    assert 0, "错误信息: {}".format(str(error))
                else:
                    raise Exception("错误信息: {}".format(str(error)))
        return wrapper


def screenshot(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Log.info("当前运行测试用例id: {} 名称: {}".format(args[0].__class__.__name__, func.__name__))
        driver = args[0].driver
        case_id = args[0].case_id
        try:
            return func(*args, **kwargs)
        except (AssertionError, Exception) as e:
            error = e
            Log.warning("{}_{}用例运行失败: {}".format(
                args[0].__class__.__name__, func.__name__, error.__str__()))
            screen(driver, func, case_id)
            if isinstance(error, AssertionError):
                assert 0, "Info: {}".format(str(error))
            else:
                raise Exception("Info: {}".format(str(error)))
    return wrapper
