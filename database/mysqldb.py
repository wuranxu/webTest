__author__ = 'Woody'
import logging

import mysql.connector as sql

from config import Config


class MysqlDb(object):
    """
        example:
        with MysqlDb() as db:
            rt = db.query(sql, params=())
    """
    host = Config.MYSQL_HOST
    port = Config.MYSQL_PORT
    user = Config.MYSQL_USER
    pwd = Config.MYSQL_PWD

    def __init__(self):
        self.conn = sql.connect(host=self.host, port=self.port,
                                user=self.user, passwd=self.pwd)
        self.cursor = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
        if exc_tb:
            print("error: ".format(str(exc_val)))

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, sql, params=()):
        rv = None
        cursor = self.cursor
        try:
            cursor.execute(sql, params)
            rv = cursor.fetchall()
        except Exception as err:
            logging.error('query error: {}'.format(str(err)))
            print(str(err))
        return rv

    def operator(self, sql, params=()):
        rv = False
        cursor = self.cursor()
        try:
            cursor.execute(sql, params)
            self.conn.commit()
            rv = True
        except Exception as err:
            logging.error('query error: {}'.format(str(err)))
            print(str(err))
        return rv

