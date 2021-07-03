import sys

import logbook

from config import Config


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@SingletonDecorator
class Log(object):
    handler = None

    def __init__(self, name='webTest', filename=Config.LOG_NAME):  # Logger标识默认为app
        """
        :param name: 业务名称
        :param filename: 文件名称
        """
        self.handler = logbook.FileHandler(filename, encoding='utf-8', bubble=True)
        self.sys_handler = logbook.StreamHandler(sys.stdout)
        logbook.set_datetime_format("local")  # 将日志时间设置为本地时间
        self.logger = logbook.Logger(name)
        self.logger.handlers.append(self.handler)
        self.logger.handlers.append(self.sys_handler)
        # self.handler.push_application()

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)
