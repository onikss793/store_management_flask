import pymysql

from config import db, test_db


def get_db_connection(test: bool = False):
    if test:
        return pymysql.connect(**test_db)
    else:
        return pymysql.connect(**db)
