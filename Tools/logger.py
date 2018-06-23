import logging
import os
import sys

from config import Config
from Tools.utils import Utils


class Logger(object):

    def __init__(self, filename=Config.LOGGER):

        # 获取logger实例，如果参数为空则返回root logger
        self.logger = logging.getLogger(filename)

        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

        # 文件日志
        Utils.make_dir(Config.LOG_DIR)
        file_handler = logging.FileHandler("{}.log".format(
            os.path.join(Config.LOG_DIR, filename)), encoding="utf-8")
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        if file_handler.baseFilename not in \
                [x.baseFilename for x in self.logger.handlers if getattr(x, "baseFilename", False)]:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        self.logger.setLevel(logging.INFO)

