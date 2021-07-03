import base64
from functools import wraps

from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import Config
from util.logger import Log
from util.web_tool import Tools

log = Log()


def wait(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info("当前Page: {} 操作: {} 控件名: {} 定位方式: [{}] 元素: [{}]".format(
            args[1].file, func.__name__, "->".join([str(x) for x in args[1:]]), args[1].method, args[1].value, ))
        try:
            WebDriverWait(args[0], Config.TIMEOUT).until(EC.element_to_be_clickable(
                (getattr(By, args[1].method), args[1].value)))
            # WebDriverWait(args[0], Config.TIMEOUT).until(
            #     lambda x: x.find_element(getattr(By, args[1].method), args[1].value).send_keys("1")
            # )
        except Exception:
            log.error("等待元素可点击超时! \n文件名: {}\n函数名: {}\n控件名: {} 定位: [{} -> {}]".format(
                args[1].file, func.__name__, args[1].name, args[1].method, args[1].value))
            assert 0, "等待元素可点击超时! \n文件名: {}\n函数名: {}\n控件名: {} 定位: [{} -> {}]".format(
                args[1].file, func.__name__, args[1].name, args[1].method, args[1].value)
        return func(*args, **kwargs)

    return wrapper


def found(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info("页面: {} 操作: {} 控件名: {}".format(
            args[1].file, func.__name__, "->".join([str(x) for x in args[1:]])))
        try:
            WebDriverWait(args[0], Config.TIMEOUT).until(EC.visibility_of_any_elements_located(
                (getattr(By, args[1].method), args[1].value)))
        except ElementNotVisibleException:
            log.error("等待元素超时! \n文件名: {}\n函数名: {}\n控件名: {} 定位: [{} -> {}]".format(
                args[1].file, func.__name__, args[1].name, args[1].method, args[1].value))
            raise ElementNotVisibleException("等待元素超时! \n文件名: {}\n函数名: {}\n控件名: {} 定位: [{} -> {}]".format(
                args[1].file, func.__name__, args[1].name, args[1].method, args[1].value))
        return func(*args, **kwargs)

    return wrapper


def generate_bs64(filename):
    with open(filename, mode='rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return b64


def update_pic_info(case_id, test_func, filename):
    if hasattr(Config, "screenshot"):
        getattr(Config, "screenshot").update({case_id + "_" + test_func: generate_bs64(filename)})
    else:
        setattr(Config, "screenshot", {case_id + "_" + test_func: generate_bs64(filename)})


def screen(driver, func, case_id, test_func):
    t = Tools(driver)
    filename = t.get_pic(func.__name__, case_id)
    update_pic_info(case_id, test_func, filename)


def pic(*params):
    if not callable(params[0]):
        re_run = params[0]

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                log.info("当前运行测试用例: {} 函数: {}".format(args[0].__class__.__name__, func.__name__))
                driver = args[0].driver
                case_id = args[0].case_id
                error = None
                for i in range(1, re_run + 1):
                    try:
                        return func(*args, **kwargs)
                    except (AssertionError, Exception) as e:
                        error = e
                        log.warning("{}_{}用例第{}次失败: {}".format(
                            args[0].__class__.__name__, func.__name__, i, error.__str__()))
                else:
                    screen(driver.page, func, case_id)
                    if isinstance(error, AssertionError):
                        assert 0, "错误信息: {}".format(str(error))
                    else:
                        raise Exception("错误信息: {}".format(str(error)))

            return wrapper

        return decorator
    else:
        @wraps(params[0])
        def wrapper(*args, **kwargs):
            log.info("当前运行测试用例id: {} 名称: {}".format(args[0].__class__.__name__, params[0].__name__))
            driver = args[0].driver
            case_id = args[0].case_id
            error = None
            for i in range(1, 3):
                try:
                    return params[0](*args, **kwargs)
                except (AssertionError, Exception) as e:
                    error = e
                    log.warning("{}_{}用例第{}次失败: {}".format(
                        args[0].__class__.__name__, params[0].__name__, i, error.__str__()))
            else:
                screen(driver.page, params[0], case_id, args[0]._testMethodName)
                if isinstance(error, AssertionError):
                    assert 0, "错误信息: {}".format(str(error))
                else:
                    raise Exception("错误信息: {}".format(str(error)))

        return wrapper


def screenshot(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info("当前运行测试用例id: {} 名称: {}".format(args[0].__class__.__name__, func.__name__))
        driver = args[0].driver
        case_id = args[0].case_id
        try:
            return func(*args, **kwargs)
        except (AssertionError, Exception) as e:
            error = e
            log.warning("{}_{}用例运行失败: {}".format(
                args[0].__class__.__name__, func.__name__, error.__str__()))
            screen(driver.page, func, case_id, args[0]._testMethodName)
            if isinstance(error, AssertionError):
                assert 0, "Info: {}".format(str(error))
            else:
                raise Exception("Info: {}".format(str(error)))

    return wrapper
