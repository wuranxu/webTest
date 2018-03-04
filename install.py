import os
import shutil
import subprocess
import zipfile

from config import Config


class Install(object):

    xmind_dir = "xmind-sdk-python-master"
    xmind_url = "https://codeload.github.com/xmindltd/xmind-sdk-python/zip/master"
    xmind_zip = "xmind.zip"
    dir = "temp"
    dir_path = os.path.join(Config.ROOT, dir)
    zip_path = os.path.join(dir_path, xmind_zip)
    if Config.SYS == "win":
        pip, py = "pip", "python"
    else:
        pip, py = "pip3", "python3"

    def mk_dir(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir)
        else:
            self.clean()

    def pip_install(self):
        os.system("{} install -r requirements.txt -i https://pypi.douban.com/simple".format(self.pip))

    def xmind_install(self):
        cmdCurrentDirectory = os.path.join(self.dir_path, self.xmind_dir)
        p = subprocess.Popen('{} setup.py install'.format(self.py), shell=True, cwd=cmdCurrentDirectory)
        retcode = p.wait()

    def run(self):
        # 建立临时目录
        self.mk_dir()

        # 安装pip
        self.pip_install()

        # 下载xmind zip
        self.get_zip()

        # 解压zip
        self.un_zip()

        # 安装xmind
        self.xmind_install()

        # 删除zip
        self.clean()

    def get_zip(self):
        try:
            import requests
            r = requests.get(self.xmind_url, timeout=20)
            with open(self.zip_path, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print("下载xmind.zip失败, 请重新运行install.py!")
            raise Exception(e.__str__())

    def un_zip(self):
        """unzip zip file"""
        with zipfile.ZipFile(self.zip_path) as f:
            for names in f.namelist():
                f.extract(names, self.dir_path)

    def clean(self):
        if os.path.exists(self.dir_path):
            shutil.rmtree(self.dir_path)


if __name__ == "__main__":
    ins = Install()
    ins.run()