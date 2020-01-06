import sqlite3
import pathlib
import os

DEFAUTL_PATH_DATABASE = pathlib.Path.home()

class DataBaseConnection():
    def __init__(self, path=DEFAUTL_PATH_DATABASE, name_db=''):
        self.path = path
        self.name_db = name_db
    
    def __connection(self):
        db = os.path.join(self.path, self.name_db)
        return sqlite3.connect(db)

    def run(self, sql, *args):
        connection = self.__connection()
        cursor = connection.cursor()

        cursor.execute(sql, args)

        connection.commit()
        connection.close()