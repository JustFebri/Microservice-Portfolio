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

    def regis(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount > 0):
            cursor.close()
            result.append("Username telah terdaftar")
            return result
        else:
            sql = "INSERT INTO user VALUES(0, '{}', '{}')".format(a, b)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registrasi berhasil")
            return result
        
    def login(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("Username tidak terdaftar")
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


    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM user_news WHERE timestamp >= DATE_SUB(curdate(), INTERVAL 30 DAY)"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'newsdesc': row['newsdesc'],
                'file': row['file']
            })
        cursor.close()
        return result
    
    def get_news(self, news):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM user_news WHERE id = {}".format(news)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def post_news(self, desc, fileName):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from user_news where file = '{}'".format(fileName)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            sql = "INSERT INTO user_news VALUES(0, '{}', '{}', CURRENT_DATE)".format(desc, fileName)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return 0
        else:
            cursor.close()
            return 1
    
    def edit_news(self, id, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from user_news where  id = '{}'".format(id)
        cursor.execute(sql)
        result = []
        if cursor.rowcount != 0:
            sql = "UPDATE user_news SET newsdesc = %s, timestamp = CURRENT_DATE WHERE id = %s"
            val  = (news, id)
            cursor.execute(sql, val)
            self.connection.commit()
            cursor.close()
            result.append("News Edited")
            return result
        else:
            result.append("Id not found")
            return result
    
    def delete_news(self, id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        
        sql = "SELECT * from user_news where  id = '{}'".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        temp = result['file']
        
        if(cursor.rowcount != 0):
            sql = "DELETE FROM user_news WHERE id = {}".format(id)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return temp
        else:
            return 0
    
    def download(self, id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from user_news where  id = '{}'".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if cursor.rowcount != 0:
            temp = result['file']
            self.connection.commit()
            cursor.close()
            return temp
        else:
            return 0
    
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
                database='deptnewsboard',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
