from sqlite3 import Cursor
from unittest import result
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def regis(self, a, b, c, d):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where nrp = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount > 0):
            cursor.close()
            result.append("NRP telah terdaftar")
            return result
        else:
            sql = "INSERT INTO user VALUES('{}', '{}', '{}', '{}')".format(a, b, c, d)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registrasi berhasil")
            return result
        
    def login(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where nrp = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("NRP tidak terdaftar")
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == b):
                cursor.close()
                result.append("Login Berhasil")
                return 1
            else:
                cursor.close()
                result.append("Password salah")
                return 0
            
    def uploadfile(self, username, fileName, judul, abstract):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from storage where filename = '{}' and abstract = '{}'".format(judul, abstract)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            sql = "INSERT INTO storage VALUES(0, '{}', '{}', '{}', '{}')".format(username, fileName, judul, abstract)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return 0
        else:
            cursor.close()
            return 1
        
    def checkUser(self, username, filename):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from storage where uploadby = '{}' and filename = '{}'".format(username, filename)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            return 0
        else:
            return 1
        
    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='dbstudent',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
