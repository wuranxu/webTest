__author__ = 'Woody'
import logging

import pymongo

from config import Config


class MongoClient(object):
    HOST = Config.MONGO_HOST
    PORT = Config.MONGO_PORT
    user = Config.MONGO_USER
    pwd = Config.MONGO_PWD
    Client = None

    def __init__(self, db="imtalk"):
        try:
            self.Client = pymongo.MongoClient(host=self.HOST, port=self.PORT, maxPoolSize=200)
            self.db = self.Client[db]
            assert self.db.authenticate(self.user, self.pwd), "mongo服务器连接失败!"
        except Exception as err:
            raise Exception("mongo connect error: {}".format(str(err)))

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.Client is not None:
            self.Client.close()
        if exc_tb:
            logging.error("error: ".format(str(exc_val)))

    def __del__(self):
        self.Client.close()

    def close(self):
        self.Client.close()
