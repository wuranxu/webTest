import os


class Utils(object):

    @staticmethod
    def make_dir(dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)