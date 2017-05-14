# coding: utf-8

import mysql.connector
import json

with open('./support/info.json') as f:
    dct = json.load(f)

class dbOper(object):

    config = {'raise_on_warnings': True, }
    config.update(dct['db_info']['info'])

    def __init__(self):
        self.cnx = mysql.connector.connect(**dbOper.config)
        self.cursor = self.cnx.cursor(dictionary=True)

    def query(self, _sql):
        try:
            self.cursor.execute(_sql)
            return self.cursor.fetchall()
        finally:
            self.teardown()

    def update(self, _sql):
        try:
            self.cursor.execute(_sql)
            self.cnx.commit()
        except Exception, e:
            self.cnx.rollback()
            raise e
        finally:
            self.teardown()

    def teardown(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except Exception, e:
            pass

if __name__ == '__main__':
    pass