import os
import re
import subprocess
import zipfile

import requests
from bs4 import BeautifulSoup

from Tools.utils import Utils
from config import Config


class Browser(object):

    @classmethod
    def set_browser(cls):
        # 自动检查Chrome版本号
        if Config.SYS == "mac":
            # OS X
            result = subprocess.Popen([r'{}/Google\ Chrome --version'.format(Config.chrome_app)], stdout=subprocess.PIPE, shell=True)
            version = [x.decode("utf-8") for x in result.stdout][0].strip().split(" ")[-1]
        elif Config.SYS == "win":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, Config.chrome_reg)
                version = winreg.QueryValueEx(key, "version")[0]    # 查询注册表chrome版本号
            except Exception:
                raise Exception("查询注册表chrome版本失败!")
        else:
            # 设置firefox浏览器信息
            result = subprocess.Popen(['/usr/bin/firefox --version'], stdout=subprocess.PIPE, shell=True)
            version = [x.decode("utf-8") for x in result.stdout][0].strip().split(" ")[-1]
            Config.browser_ver = version
            return
        Config.browser_ver = version
        file_vr = cls.search_ver(version)
        if file_vr is None:
            raise Exception("未获取到chrome版本号! 请检查!")
        status, file = cls.check_driver(file_vr)
        if not status:
            cls.gen_driver(file_vr)
        else:
            print("系统已存在chromedriver, 无需下载!")
            Config.DRIVER_PATH = os.path.join(Config.driver_dir, file)

    @classmethod
    def check_driver(cls, version):
        status, filename = False, None
        Utils.make_dir(Config.driver_dir)    # check driver_dir
        for root, dirs, files in os.walk(Config.driver_dir):
            for file in files:
                if version not in file:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
                else:
                    status, filename = True, file
        return status, filename

    @classmethod
    def search_ver(cls, version):
        if version != "unknown":
            number = version.split(".")[0]
            file_vr = None
            url = Config.driver_url + "LATEST_RELEASE"
            r = requests.get(url)
            bs = BeautifulSoup(r.text)
            latest = bs.text.strip()
            record = "{}/{}/notes.txt".format(Config.driver_url, latest)
            info = requests.get(record)
            text = info.text
            vr = re.findall(r"-+ChromeDriver\s+v(\d+\.+\d+)[\s|.|-|]+", text)
            br = re.findall(r"Supports\s+Chrome\s+v(\d+-\d+)", text)
            for v, b in zip(vr, br):
                small, bigger = b.split("-")
                if int(small) <= int(number) <= int(bigger):
                    # 找到版本号
                    print("找到浏览器对应驱动版本号: {}".format(v))
                    file_vr = v
                    break
            return file_vr

    @classmethod
    def gen_driver(cls, file_vr):
        if Config.SYS == "mac":
            file = "chromedriver_mac64.zip".format(file_vr)
            driver = "chromedriver"
        elif Config.SYS == "win":
            file = "chromedriver_win32.zip".format(file_vr)
            driver = "chromedriver.exe"
        else:
            file = "chromedriver_linux64.zip".format(file_vr)
            driver = "chromedriver"
        r = requests.get("{}{}/{}".format(Config.driver_url, file_vr, file))
        file_path = os.path.join(Config.driver_dir, file)
        print("开始下载!")
        with open(file_path, "wb") as f:
            f.write(r.content)
        cls.unzip_driver(file)
        cls.change_driver_name(file_vr, driver)

    @classmethod
    def unzip_driver(cls, filename):
        if Config.SYS == "mac":
            # 解压zip
            os.system('cd {};unzip {}'.format(Config.driver_dir, filename))
        elif Config.SYS == "win":
            cls.unzip_win(os.path.join(Config.driver_dir, filename))
        else:
            pass

    @classmethod
    def change_driver_name(cls, version, filename):
        if Config.SYS == "mac":
            new_file = "{}_{}".format(filename, version)
        elif Config.SYS == "win":
            L = filename.split(".")
            new_file = "{}_{}.{}".format("".join(L[:-1]), version, L[-1])
        else:
            new_file = ""           #TODO
        os.rename(os.path.join(Config.driver_dir, filename),
                  os.path.join(Config.driver_dir, new_file))
        Config.DRIVER_PATH = os.path.join(Config.driver_dir, new_file)

    @classmethod
    def unzip_win(cls, filename):
        """unzip zip file"""
        with zipfile.ZipFile(filename) as f:
            for names in f.namelist():
                f.extract(names, Config.driver_dir)